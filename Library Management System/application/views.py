from flask import current_app as app, render_template, jsonify, request, send_file
from flask_security import auth_required, roles_required, current_user
from .sec import datastore
from .models import db, User, Section, EBook, IssueReturn, Ratings, Role, RolesUsers
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import cast, Date, or_, func, and_
import flask_excel as excel
from celery.result import AsyncResult
from .tasks import create_resource_csv, send_notification
from .mail_service import send_email
from .instances import cache
from datetime import datetime, timedelta
import pytz
import random

IST = pytz.timezone('Asia/Kolkata')

def randomColor(alpha): # transparency
    red = random.randint(0,255)
    blue = random.randint(0,255)
    green = random.randint(0,255)
    return 'rgba'+str((red, green, blue, alpha))

@app.get("/")
def home():
    return render_template('index.html')

#---------------AUTHENTICATION--------------------
@app.post('/userregister')
def userregister():
    try:
        data = request.get_json()
        username = data.get('username')
        fullname = data.get('fullname')
        email = data.get('email')
        role = data.get('role')
        password = data.get('password')
        if not username:
            return jsonify({"message": "Username not provided!"}), 400
        if not email:
            return jsonify({"message": "Email not provided!"}), 400
        if not datastore.find_user(email=email):
            datastore.create_user(email=email, username=username, full_name=fullname, password=generate_password_hash(password), roles=['general_user'],active=True)
            db.session.commit()
            return jsonify({'message': 'User registered successfully! Proceed to login.'}), 200
        else:
            return jsonify({"message": "This email is already registered!"}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to register user.'}), 500

@app.post('/userlogin')
def userlogin():
    try:
        data = request.get_json()
        email = data.get('email')
        role = data.get('role')
        if not email:
            return jsonify({"message": "Email not provided!"}), 400
        if not role:
            return jsonify({"message": "Role not provided!"}), 400
        user = datastore.find_user(email=email)
        if not user:
            return jsonify({"message": "User not found!"}), 404
        print(role, user.roles[0].name)
        if role != user.roles[0].name:
            return jsonify({"message": "Not Authorized!"}), 403
        if check_password_hash(user.password, data.get("password")):
            user.last_activity = datetime.now(IST)
            db.session.commit()
            return jsonify({"token": user.get_auth_token(), "email": user.email, "username": user.username, "full_name": user.full_name, "role": user.roles[0].name}), 200
        else:
            return jsonify({"message": "Incorrect password!"}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to login.'}), 500
    
@app.post('/forgotpassword')
def forgotpassword():
    try:
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"message": "Email not provided!"}), 400
        user = datastore.find_user(email=email)
        if not user:
            return jsonify({"message": "Email not registered!"}), 404
        otp = random.randint(1000,9999)
        send_email(email, "OTP for Password Reset",f'''
                   Dear {user.username},
                   Your OTP to reset password is {otp}. 
                   Please enter this on the LMS to proceed to set a new password.
                   
                   Regards,
                   LMS
                   ''')
        details = {
            'email': email,
            'otp': otp,
        }
        return jsonify({'details': details}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to verify email.'}), 500
    
@app.post('/resetpwd')
def resetpwd():
    try:
        data = request.get_json()
        email = data.get('email')
        newpassword = data.get('newpassword')
        if not email:
            return jsonify({"message": "Email not provided!"}), 400
        if not newpassword:
            return jsonify({"message": "Password not provided!"}), 400
        user = datastore.find_user(email=email)
        if not user:
            return jsonify({"message": "User not found!"}), 404
        user.password = generate_password_hash(newpassword)
        db.session.commit()
        return jsonify({'message': 'Password reset successfully.'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to set new password.'}), 500

@app.post('/editprofile')
@auth_required('token')
def editprofile():
    try:
        user = current_user
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        full_name = data.get('full_name')
        if not username:
            return jsonify({"message": "Username not provided!"}), 400
        if not email:
            return jsonify({"message": "Email not provided!"}), 400
        if not full_name:
            return jsonify({"message": "Name not provided!"}), 400
        searched_user = datastore.find_user(email=email)
        if (searched_user and searched_user.id!=user.id):
            return jsonify({'message': 'This email is already in use.'}), 400
        searched_uname = datastore.find_user(username=username)
        if (searched_uname and searched_uname.id!=user.id):
            return jsonify({'message': 'This username is already in use.'}), 400
        else:
            user.username = username
            user.full_name = full_name
            user.email = email
            db.session.commit()
            newdetail={
                'username': username,
                'email': email,
                'full_name': full_name,
                'message': 'Profile edited successfully.'
            }
            return jsonify({'newdetail': newdetail}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to edit profile.'}), 500
    
#---------------------SECTIONS (edit/delete)-------------------------
# get section for edit
@app.get('/getsection')
@auth_required('token')
@roles_required('librarian')
def getsection():
    try:
        secid = request.args.get('secid')
        section = Section.query.get(secid)
        if section:
            section_data={'id': section.id, 
                        'section_name': section.section_name, 
                        'desc': section.description,
                        'icon': section.section_icon}
            return jsonify({"section_data": section_data}), 200
        else:
            return jsonify({"message": "Section not found!"}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch Section details.'}), 500

#--------------------------E-Books--------------------------------
@app.get('/all_ebooks') # view all ebookss
@auth_required('token')
@cache.cached(timeout=300, key_prefix='ebooks')
def all_ebooks():
    try:
        user = current_user
        ebooks = db.session.query(EBook.id, EBook.book_name, EBook.author, Section.section_name, IssueReturn.id.label('reqid'), IssueReturn.status).join(Section, EBook.section_id==Section.id).outerjoin(IssueReturn, (EBook.id == IssueReturn.ebook_id) & (IssueReturn.user_id == user.id)).all()
        print(ebooks)
        all_ebooks = [{'id': bk.id,
                       'reqid': bk.reqid,
                       'book_name': bk.book_name,
                       'author': bk.author,
                       'status': bk.status,
                       'section_name': bk.section_name} for bk in ebooks]
        return jsonify({'ebooks': all_ebooks}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch books.'}), 500

# section wise ebooks
@app.get('/ebooks') # view ebooks in a section
@auth_required('token')
# @cache.cached(timeout=300, key_prefix='ebooks')
def ebooks():
    try:
        user = current_user
        section_id = request.args.get('section_id')
        section = Section.query.filter_by(id=section_id).first()
        ebooks = db.session.query(EBook.id, EBook.book_name, EBook.author, IssueReturn.status).join(Section, EBook.section_id==Section.id).outerjoin(IssueReturn, (EBook.id == IssueReturn.ebook_id) & (IssueReturn.user_id == user.id)).filter(EBook.section_id == section_id).all()
        all_ebooks = [{'id': bk.id,
                       'book_name': bk.book_name,
                       'author': bk.author,
                       'status': bk.status} for bk in ebooks]
        return jsonify({'ebooks': all_ebooks},{'section_name': section.section_name}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch books.'}), 500

@app.post('/addebook') # add new ebook
@auth_required('token')
@roles_required('librarian')
def addebook():
    try:
        user = current_user
        data = request.get_json()
        section_id = data.get('section_id')
        book_name = data.get('book_name')
        author = data.get('author')
        content = data.get('content')
        if not book_name:
            return jsonify({"message": "EBook name not provided!"}), 400
        new_ebook = EBook(section_id=section_id,book_name=book_name, author=author, content=content, created_by=user.username)
        db.session.add(new_ebook)  
        db.session.commit()
        return jsonify({'message': 'EBook created successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to add book.'}), 500

@app.post('/editebook') # edit ebook
@auth_required('token')
@roles_required('librarian')
def editebook():
    try:
        user = current_user
        bookid = request.args.get('bookid')
        data = request.get_json()
        section_id = data.get('section_id')
        book_name = data.get('book_name')
        author = data.get('author')
        content = data.get('content')
        book = EBook.query.get(bookid)
        if not book:
            return jsonify({"message": "EBook not found!"}), 400
        book.section_id = section_id
        book.book_name = book_name
        book.author = author
        book.content = content
        book.updated_by = user.username
        db.session.commit()
        return jsonify({'message': 'EBook edited successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to edit book.'}), 500
    
@app.post('/deleteebook') # delete a book
@auth_required('token')
@roles_required('librarian')
def deleteebook():
    try:
        bookid = request.args.get('bookid')
        book = EBook.query.get(bookid)
        if not book:
            return jsonify({"message": "EBook not found!"}), 400
        db.session.delete(book)
        db.session.commit()
        cache.clear()
        return jsonify({'message': 'EBook deleted.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to delete EBook.'}), 500

#-------------------LIBRARIAN FUNCTIONALITIES---------------------
@app.get('/book_requests')
@auth_required('token')
@roles_required('librarian')
def book_requests():
    try:
        all_requests = []
        books_requested = db.session.query(IssueReturn.id,IssueReturn.date_created,IssueReturn.status,EBook.id.label('bookid'),EBook.book_name,User.full_name).join(EBook, IssueReturn.ebook_id==EBook.id).join(User, IssueReturn.user_id==User.id).filter(IssueReturn.status=="requested").all()
        for request in books_requested:
            book_requests = {
                    'id': request.id, # id of request
                    'bookid': request.bookid, # id of book in request
                    'user_name': request.full_name,
                    'book_name': request.book_name,
                    'request_date': request.date_created.strftime("%d-%m-%Y %I:%M %p"),
                    'status': request.status
                }
            all_requests.append(book_requests)
        return jsonify({'all_requests': all_requests}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch book requests.'}), 500
    
def default_return_date(issue_date):
    return issue_date + timedelta(days=7)

@app.post('/approve_request')
@auth_required('token')
@roles_required('librarian')
def approve_request():
    try:
        user = current_user
        reqid = request.args.get('reqid')
        book_request = IssueReturn.query.filter_by(id=reqid).first()
        print(book_request)
        already_issued = db.session.query(IssueReturn).filter(IssueReturn.ebook_id==book_request.ebook_id,IssueReturn.status=="issued").all()
        print(already_issued)
        if already_issued:
            return jsonify({'message': 'This book is already issued.'}), 400
        else:
            if book_request:
                book_request.status="issued"
                book_request.issue_date = datetime.now(IST)
                book_request.return_date = default_return_date(issue_date=datetime.now(IST))
                print(book_request.return_date, book_request.ebook_id)
                book_request.updated_by = user.username
                db.session.commit()
                
                other_requests_same_book = db.session.query(IssueReturn).filter(IssueReturn.ebook_id==book_request.ebook_id,IssueReturn.status=='requested',IssueReturn.user_id!=user.id).all()
                print(other_requests_same_book)
                if other_requests_same_book:
                    for bk in other_requests_same_book:
                        bk.status = "rejected"
                        book_request.updated_by = user.username
                        db.session.commit()
                return jsonify({'message': 'Book request granted.'}), 200
            else:
                return jsonify({'message': 'Book request not found.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to grant request.'}), 500 
    
@app.post('/reject_request')
@auth_required('token')
@roles_required('librarian')
def reject_request():
    try:
        user = current_user
        reqid = request.args.get('reqid')
        book_request = IssueReturn.query.filter_by(id=reqid).first()
        if book_request:
            book_request.status="rejected"
            book_request.updated_by = user.username
            db.session.commit()
            return jsonify({'message': 'Book request rejected.'}), 200
        else:
            return jsonify({'message': 'Book request not found.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to reject request.'}), 500 
    
@app.post('/revoke_access')
@auth_required('token')
@roles_required('librarian')
def revoke_access():
    try:
        user = current_user
        reqid = request.args.get('reqid')
        book_request = IssueReturn.query.filter_by(id=reqid).first()
        if book_request:
            book_request.status="returned"
            book_request.returned_on = datetime.now(IST)
            book_request.updated_by = user.username
            db.session.commit()
            return jsonify({'message': 'Book access revoked.'}), 200
        else:
            return jsonify({'message': 'Book request not found.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to revoke access.'}), 500 

#  LIBRARIAN DASHBOARD
@app.get('/lib_section') # view sections
@auth_required('token')
@roles_required('librarian')
# @cache.cached(timeout=300, key_prefix='lib_sections')
def lib_section():
    try:
        sections = Section.query.limit(6).all()
        all_sections = [{'id': section.id, 'section_name': section.section_name, 'section_icon': section.section_icon, 'description': section.description} for section in sections]
        return jsonify({'sections': all_sections},), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch section.'}), 500

@app.get('/lib_bookrequests')
@auth_required('token')
@roles_required('librarian')
def lib_bookrequests():
    try:
        all_requests = []
        books_requested = (IssueReturn.query.filter(IssueReturn.status == "requested").order_by(IssueReturn.date_created.desc()).limit(6).all())
        for request in books_requested:
            user = User.query.get(request.user_id)
            ebook = EBook.query.get(request.ebook_id)
            if user and ebook:
                book_requests = {
                    'id': request.id, # id of request
                    'bookid': ebook.id, # id of book in request
                    'user_name': user.full_name,
                    'book_name': ebook.book_name,
                    'author': ebook.author,
                    'request_date': request.date_created.strftime("%d-%m-%Y %I:%M %p") if request.date_created else request.date_created,
                    'status': request.status
                }
                all_requests.append(book_requests)
        return jsonify({'book_requests': all_requests}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch book requests.'}), 500

@app.get('/lib_stats') 
@auth_required('token')
@roles_required('librarian')
def lib_stats():
    try:
        user = current_user
        # number stats
        active_users = db.session.query(func.count(User.id)).join(RolesUsers, User.id == RolesUsers.user_id).join(Role, RolesUsers.role_id == Role.id).filter(User.active == True, Role.name == 'general_user').scalar()
        grant_requests = db.session.query(func.count(IssueReturn.id)).filter(IssueReturn.issue_date != None).scalar()
        ebooks_issued = db.session.query(func.count(IssueReturn.id)).filter_by(status="issued").scalar()
        ebooks_revoked = db.session.query(func.count(IssueReturn.id)).filter(IssueReturn.status=="returned",IssueReturn.updated_by==user.username).scalar() # updated by librarian
        # bar chart
        today = datetime.today()
        # print("today: ",today)
        start_date = today - timedelta(days=6)
        # print("Start date: ",start_date)
        days=[]
        issue_counts = []
        issues = db.session.query(func.strftime('%w', IssueReturn.issue_date).label('day'),func.count(IssueReturn.id).label('issue_count')).filter(IssueReturn.issue_date >= start_date, IssueReturn.issue_date <= today).group_by('day').all()
        # print(issues)
        if issues:
            # print("start weekday ",start_date.weekday())   Mon - Sun  0 -> 6
            # print("today weekday ",today.weekday())         Mon 0, Tue 1, Wed 2 etc...
            # Initialize arrays for day names according to .weekday() indexing
            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            # for i in range(7):
            #     print("index: ",i, " : ",(start_date + timedelta(days=i)).weekday(), " : " ,day_names[(start_date + timedelta(days=i)).weekday()])
            #     pass
            days = [day_names[(start_date + timedelta(days=i)).weekday()] for i in range(7)]
            print(days)

            # %w - used in query
            # 0 for Sunday, 1 for Monday, 2 for Tuesday, 3 for Wednesday
            # 4 for Thursday, 5 for Friday, 6 for Saturday
            issue_counts = [0,0,0,0,0,0,0]
            wkday_names = ['Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            for issue in issues:
                weekday = issue.day
                count = issue.issue_count
                # print(weekday)
                # print(count)
                get_day = wkday_names[int(weekday)]
                # print("day: ",get_day)
                get_index = days.index(get_day)
                # print("new index: ", get_index)
                issue_counts[get_index] = count
            # print(days)
            # print(issue_counts)    
            
        # doughnut chart
        sections = []
        ebook_counts = []
        colors = []
        section_ebooks = db.session.query(Section.section_name, func.count(EBook.id).label('ebook_count')).join(EBook, Section.id==EBook.section_id).group_by(Section.id).all()
        if section_ebooks:
            for sec in section_ebooks:
                sections.append(sec.section_name)
                ebook_counts.append(sec.ebook_count)
                colors.append(randomColor(alpha=0.5))
                
        
        stats = {
            'active_users': active_users,
            'grant_requests': grant_requests,
            'books_issued': ebooks_issued,
            'books_revoked': ebooks_revoked,
            'weekdays': days,
            'issue_counts': issue_counts,
            'sections': sections,
            'ebook_counts': ebook_counts,
            'sec_colors': colors
        }
        return jsonify({'stats': stats}), 200 
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch any statistics.'}), 500
    
@app.get('/users') 
@auth_required('token')
@roles_required('librarian')
@cache.cached(timeout=500, key_prefix='users')
def users():
    try:
        usersdata = db.session.query(User.id, User.full_name, User.email, User.active, User.last_activity).join(RolesUsers, User.id == RolesUsers.user_id).join(Role, RolesUsers.role_id == Role.id).filter(Role.name == 'general_user').all()
        print(usersdata)
        users = []
        if usersdata:
            for data in usersdata:
                print(data.active)
                status = "Active" if data.active else "Inactive"
                users.append({
                        'id': data.id,
                        'full_name': data.full_name,
                        'email': data.email,
                        'is_active': status,
                        'last_activity': data.last_activity.strftime("%d-%m-%Y %I:%M %p") if data.last_activity else data.last_activity
                    })
            print(users)
            return jsonify({'users': users}), 200 
        else:
           return jsonify({'message': 'No user data found.'}), 404 
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch users.'}), 500

@app.get('/issue_history')
@auth_required('token')
@roles_required('librarian')
@cache.cached(timeout=300, key_prefix='issue_history')
def issue_history():
    try:
        book_requests = db.session.query(EBook.id, EBook.book_name, Section.section_name, IssueReturn.status, IssueReturn.issue_date, IssueReturn.returned_on, IssueReturn.date_created, User.full_name, User.id.label('userid')).join(Section, EBook.section_id == Section.id).join(IssueReturn, EBook.id == IssueReturn.ebook_id).join(User, IssueReturn.user_id == User.id).all()
        issues_history = []
        if book_requests:
            for book in book_requests:
                issues_history.append({
                    'id': book.id,
                    'book_name': book.book_name,
                    'section_name': book.section_name,
                    'status': book.status,
                    'issue_date': book.issue_date.strftime("%d-%m-%Y %I:%M %p") if book.issue_date else book.issue_date,
                    'returned_on': book.returned_on.strftime("%d-%m-%Y %I:%M %p") if book.returned_on else book.returned_on,
                    'full_name': book.full_name,
                    'request_on': book.date_created.strftime("%d-%m-%Y %I:%M %p") if book.date_created else book.date_created
                })
            return jsonify({'issues_history': issues_history}), 200
        pass
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch history.'}), 500  
    
#-----------------------------USER FUNCTIONALITIES---------------------------------------
@app.get('/my_ebooks')
@auth_required('token')
@roles_required('general_user')
def my_ebooks():
    try:
        user = current_user
        issued_books = db.session.query(EBook.id, EBook.book_name, EBook.author, Section.section_name, IssueReturn.status, IssueReturn.date_created).join(Section, EBook.section_id == Section.id).join(IssueReturn, (EBook.id == IssueReturn.ebook_id) & (IssueReturn.user_id == user.id)).filter(or_(IssueReturn.status == "requested",IssueReturn.status == "rejected", IssueReturn.status == "issued")).all()
        all_issued_books = [{'id': ibk.id, 
                            'book_name': ibk.book_name, 
                            'author': ibk.author, 
                            'section_name': ibk.section_name,
                            'status': ibk.status,
                            'request_on': ibk.date_created.strftime("%d-%m-%Y %I:%M %p")} for ibk in issued_books]
        return jsonify({'issued_books': all_issued_books}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch books.'}), 500

@app.post('/request_ebook')
@auth_required('token')
@roles_required('general_user')
def request_ebook():
    try:
        user = current_user
        print(user)
        bookid = request.args.get('bookid')
        issue_count = db.session.query(func.count(IssueReturn.id)).filter_by(user_id=user.id,status="issued").scalar()
        print(issue_count)
        existing_user_req = IssueReturn.query.filter_by(user_id=user.id,ebook_id=bookid,status="issued").first()
        print(existing_user_req)
        existing_issue = IssueReturn.query.filter_by(ebook_id=bookid,status="issued").first()
        print(existing_issue)
        existing_req = IssueReturn.query.filter_by(ebook_id=bookid,user_id=user.id,status="requested").first()
        print(existing_req)
        
        if issue_count >= 5:
            return jsonify({'message': "You cannot issue more than 5 books at a time."}), 400
        
        elif existing_user_req:
            return jsonify({'message': "This book is already issued by you."}), 400
        elif existing_req:
            return jsonify({'message': "This book is already requested by you."}), 400
        elif existing_issue:
            return jsonify({'message': "This book is currently issued."}), 400
        else:
            new_req = IssueReturn(user_id=user.id,ebook_id=bookid,created_by=user.username)
            db.session.add(new_req)
            db.session.commit()
            cache.clear()
            return jsonify({'message': "Request sent."}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to add book request'}), 500
    
@app.post('/return_ebook')
@auth_required('token')
@roles_required('general_user')
def return_ebook():
    try:
        user = current_user
        bookid = request.args.get('bookid')
        issued_book = IssueReturn.query.filter_by(user_id=user.id,ebook_id=bookid,status="issued").first()
        if issued_book:
            issued_book.status = "returned"
            issued_book.returned_on = datetime.now(IST)
            issued_book.updated_by = user.username
            db.session.commit()
            return jsonify({'message': 'Book returned successfully.'}), 200
        else:
            return jsonify({'message': 'Issued book record not found.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to return book.'}), 500
    
@app.get('/read_ebook')
@auth_required('token')
def read_ebook():
    try:
        bookid = request.args.get('bookid')
        book = EBook.query.filter_by(id=bookid).first()
        print(book, bookid)
        if book:
            section = Section.query.get(book.section_id)
            print(section)
            # db.session.query(EBook, Section).join(Section, EBook.section_id == Section.id).filter(EBook.id == bookid).first()
            book_data={'id': book.id, 
                        'book_name': book.book_name, 
                        'content': book.content,
                        'author': book.author, 
                        'section_id': book.section_id,
                        'section_name': section.section_name}
            return jsonify({"book_data": book_data}), 200
        else:
            return jsonify({"message": "EBook not found!"}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch book.'}), 500

@app.post('/rateebook')
@auth_required('token')
@roles_required('general_user')
def rateebook():
    try:
        user = current_user
        data = request.get_json()
        bookid = data.get('bookid')
        rating = data.get('value')
        exist_rating = Ratings.query.filter_by(user_id=user.id, ebook_id=bookid).first()
        if exist_rating:
            exist_rating.rating = rating
            exist_rating.updated_by = user.username
            db.session.commit()
        else:
            new_rating = Ratings(user_id=user.id, ebook_id=bookid, rating=rating, created_by=user.id)
            db.session.add(new_rating)  
            db.session.commit()
        return jsonify({'message': 'Book rated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to rate book.'}), 500 

@app.get('/getrating')
@auth_required('token')
# @roles_required('general_user')
def getrating():
    try:
        user = current_user
        bookid = request.args.get('bookid')
        rating = Ratings.query.filter_by(user_id=user.id, ebook_id=bookid).first()
        if rating:
            return jsonify({"rating": rating.rating}), 200
        else:
            return jsonify({"rating": 0}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch rating.'}), 500 

# USER DASHBOARD
@app.get('/user_stats') 
@auth_required('token')
@roles_required('general_user')
def user_stats():
    try:
        user = current_user
        books_read = db.session.query(func.count(IssueReturn.id)).filter(IssueReturn.issue_date != None,IssueReturn.user_id==user.id).scalar()
        ebooks_issued = db.session.query(func.count(IssueReturn.id)).filter(IssueReturn.status=="issued",IssueReturn.user_id==user.id).scalar()
        ebooks_requested = db.session.query(func.count(IssueReturn.id)).filter(IssueReturn.status=="requested",IssueReturn.user_id==user.id).scalar()
        ebooks_rejected = db.session.query(func.count(IssueReturn.id)).filter(IssueReturn.status=="rejected",IssueReturn.user_id==user.id).scalar()
        #books_rated = db.session.query(func.count(Ratings.id)).filter(Ratings.user_id == user.id).scalar()
        
        # bar chart
        book_names = []
        avg_ratings = []
        top_five_books = db.session.query(EBook.book_name,func.avg(Ratings.rating).label('average_rating')).outerjoin(Ratings, EBook.id==Ratings.ebook_id).group_by(EBook.id).order_by(func.avg(Ratings.rating).desc()).limit(5).all()
        if top_five_books:
            for i in range(len(top_five_books)):
                book = top_five_books[i]
                book_names.append(book.book_name)
                avg_ratings.append(book.average_rating)
        
        # doughnut chart
        sections = []
        ebook_counts = []
        colors = []
        section_ebooks = db.session.query(Section.section_name, func.count(EBook.id).label('ebook_count')).join(EBook, Section.id==EBook.section_id).join(IssueReturn, IssueReturn.ebook_id==EBook.id).filter(IssueReturn.issue_date != None,IssueReturn.user_id==user.id).group_by(Section.id).all()
        if section_ebooks:
            for sec in section_ebooks:
                sections.append(sec.section_name)
                ebook_counts.append(sec.ebook_count)
                colors.append(randomColor(alpha=0.5))
        print(sections, ebook_counts)
        
        stats = {
            'books_read': books_read,
            'ebooks_rejected': ebooks_rejected,
            'books_issued': ebooks_issued,
            'books_requested': ebooks_requested,
            'book_names': book_names,
            'avg_ratings': avg_ratings,
            'sections': sections,
            'ebook_counts': ebook_counts,
            'sec_colors': colors
        }
        return jsonify({'stats': stats}), 200 
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Failed to fetch any statistics.'}), 500

@app.get('/search')
@auth_required('token')
def search():
    user = current_user
    query = request.args.get('query')
    if query:
        
        books = db.session.query(EBook.id, EBook.book_name, EBook.author, EBook.section_id, IssueReturn.status).outerjoin(IssueReturn, (EBook.id == IssueReturn.ebook_id) & (IssueReturn.user_id == user.id)).filter(or_(EBook.book_name.ilike(f'%{query}%'), EBook.author.ilike(f'%{query}%'))).all()
        sections = Section.query.filter(Section.section_name.ilike(f'%{query}%')).all()
        
        if books or sections:
        
            books_data = []
            section_data = []
            
            if books:
                for book in books:
                    section = Section.query.get(book.section_id)
                    book_result = {
                        'id': book.id,
                        'book_name': book.book_name,
                        'author': book.author,
                        'section_name': section.section_name,
                        'status': book.status
                    }
                    books_data.append(book_result)
            if sections:
                section_data = [{'id': section.id,
                                'section_name': section.section_name, 
                                'section_icon': section.section_icon, 
                                'description': section.description} for section in sections]
            results = {
                'books': books_data,
                'sections': section_data
            }
            return jsonify({'results': results},), 200
        else:
            return jsonify({'message': 'No matching results found.'}), 400

@app.get('/search_ebook')
@auth_required('token')
def search_ebook():
    user = current_user
    query = request.args.get('query')
    if query:
        books = db.session.query(EBook.id, EBook.book_name, EBook.author, EBook.section_id, IssueReturn.status).outerjoin(IssueReturn, (EBook.id == IssueReturn.ebook_id) & (IssueReturn.user_id == user.id)).filter(or_(EBook.book_name.ilike(f'%{query}%'), EBook.author.ilike(f'%{query}%'))).all()
        books_data = []
        
        if books:
            for book in books:
                section = Section.query.get(book.section_id)
                book_result = {
                    'id': book.id,
                    'book_name': book.book_name,
                    'author': book.author,
                    'section_name': section.section_name,
                    'status': book.status
                }
                books_data.append(book_result)
            return({'books': books_data}), 200
        else:
            return jsonify({'message': 'Please enter a term to search.'}), 400