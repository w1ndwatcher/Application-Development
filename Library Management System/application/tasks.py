from celery import shared_task
from .models import EBook, Section, IssueReturn, db, User, Role, RolesUsers, Ratings
import flask_excel as excel
from .mail_service import send_email
from json import dumps
from httplib2 import Http
from datetime import datetime, timedelta
import pytz
from sqlalchemy import func, and_
from jinja2 import Template

IST = pytz.timezone('Asia/Kolkata')

@shared_task(ignore_result=True)
def auto_revoke():
    IST = pytz.timezone('Asia/Kolkata')
    today = datetime.now(IST).date()
    books_to_return = db.session.query(IssueReturn).filter(IssueReturn.status=='issued', func.date(IssueReturn.return_date)==today).all()
    print(books_to_return)
    for book in books_to_return:
        print(book)
        book.status = 'returned'
        book.returned_on = datetime.now(IST)
        book.updated_by = 'lms'
        db.session.commit()
    return "Auto-Revoke Complete"
        
    
@shared_task(ignore_result=False)
def create_resource_csv():
    book_requests = db.session.query(EBook.book_name, EBook.author, EBook.content, Section.section_name, IssueReturn.status, IssueReturn.issue_date, IssueReturn.returned_on, User.full_name).join(Section, (EBook.section_id == Section.id)).join(IssueReturn, (EBook.id == IssueReturn.ebook_id)).join(User, (IssueReturn.user_id == User.id)).all()
    csv_output = excel.make_response_from_query_sets(book_requests, ["book_name","author","content", "section_name","status","issue_date","returned_on","full_name"], "csv", filename="test1.csv")
    today = datetime.now(IST)
    filename = f"{today}_report.csv"
    with open(filename, 'wb') as f:
        f.write(csv_output.data)
    return filename


@shared_task(ignore_result=True)
def monthly_report():
    today = datetime.today()
    first_day_current_month = today.replace(day=1)
    last_day_current_month = today.replace(day=30)  # for testing
    last_day_last_month = first_day_current_month - timedelta(days=1)
    last_month = last_day_last_month.strftime('%b %Y')  # for report heading
    first_day_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)
    
    librarian = db.session.query(User.full_name,User.email).join(Role, User.id == RolesUsers.user_id).join(RolesUsers, RolesUsers.role_id == Role.id).filter(Role.name == 'librarian').first()
    
    book_requests = db.session.query(EBook.id, EBook.book_name, Section.section_name, IssueReturn.status, IssueReturn.issue_date, IssueReturn.returned_on, User.full_name, User.id.label('userid')).join(Section, EBook.section_id == Section.id).join(IssueReturn, EBook.id == IssueReturn.ebook_id).join(User, IssueReturn.user_id == User.id).filter(
            and_(
                IssueReturn.date_created >= first_day_last_month,  # IssueReturn.date_created >= first_day_current_month,
                IssueReturn.date_created <= last_day_last_month    # IssueReturn.date_created <= last_day_current_month
            )
        ).all()

    books_with_ratings = []
    
    if book_requests:
        for book in book_requests:
            rating = 0
            rating_query = db.session.query(Ratings.rating).filter(Ratings.ebook_id==book.id, Ratings.user_id==book.userid).scalar()
            if rating_query:
                rating = rating_query
            books_with_ratings.append({
                'id': book.id,
                'book_name': book.book_name,
                'section_name': book.section_name,
                'status': book.status,
                'issue_date': book.issue_date.strftime("%d-%m-%Y %I:%M %p") if book.issue_date else book.issue_date,
                'returned_on': book.returned_on.strftime("%d-%m-%Y %I:%M %p") if book.returned_on else book.returned_on,
                'full_name': book.full_name,
                'rating': rating
            })
        with open('templates/report.html', 'r') as f:
            template = Template(f.read())
            send_email(librarian.email, "Monthly Activity Report", template.render(bwr = books_with_ratings,last_month=last_month))
        return "Monthly Report Complete"
    else:
        return "No activity logged for last month."


@shared_task(ignore_result=False)
def daily_reminder():
    cutoff_time = datetime.now(IST) - timedelta(hours = 24)   # not visited in last 24 hours
    users_not_visited = db.session.query(User.full_name).join(Role, User.id == RolesUsers.user_id).join(RolesUsers, RolesUsers.role_id == Role.id).filter(Role.name == 'general_user', User.last_activity > cutoff_time).all()
    print("NV: ",users_not_visited)
    return_date_approaching = db.session.query(EBook.book_name, IssueReturn.return_date, User.full_name).join(IssueReturn, EBook.id == IssueReturn.ebook_id).join(User, IssueReturn.user_id == User.id).filter(IssueReturn.status == 'issued', IssueReturn.return_date > datetime.now(IST)).all()
    print("RDA: ",return_date_approaching)
    if users_not_visited:
        for user in users_not_visited:
            unv_message = f"Hello {user.full_name}, we miss you! Please visit the app and checkout the extensive book collection we have for you."
            send_notification(unv_message)
    if return_date_approaching:
        for user in return_date_approaching:
            rda_message = f"Hello {user.full_name}, your issued book '{user.book_name}' is due to return on {user.return_date.strftime('%d-%m-%Y')}. Please return the book before the due date to avoid any fine."
            send_notification(rda_message)

# https://chat.googleapis.com/v1/spaces/AAAALZbXyGM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=PPj7rlGlPZEDw1A04zr81BzdQ5_Oo9Qv0mnWBQFRYzw
def send_notification(msg):
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAAALZbXyGM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=PPj7rlGlPZEDw1A04zr81BzdQ5_Oo9Qv0mnWBQFRYzw"
    app_message = {"text": msg}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    return "G-Chat Complete"