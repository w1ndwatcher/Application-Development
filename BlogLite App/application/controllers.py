from flask import Flask, request, flash, session,Blueprint
from flask import render_template, redirect, url_for
from flask import current_app as app
from . import db
from application.models import User,Post,Comment,Like
import os
import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
views = Blueprint('views', __name__)


now = datetime.datetime.now()
currenttime = now.strftime("%d%m%Y%H%M%S")

@views.route("/", methods=["GET", "POST"])
@login_required
def homepage():
    q=request.args.get('search')
    if q:
        posts = Post.query.filter(Post.post_title.contains(q)| Post.post_caption.contains(q))
    else:
        posts = Post.query.order_by((Post.posted_date.desc())).all()
    colors=["#cdd6ff","#ffebcd", "#ffcdcd", "#decdff"]
    i=0
    for item in posts:
        print(type(item.author))
        item.color=colors[i]
        print(type(item))
        i+=1
        if i==4:
            i=0
    post_count=len(Post.query.filter_by(author=current_user.user_id).all())
    followers_count=current_user.followed.count()
    following_count= current_user.followers.count() 
    return render_template("dashboard.html",user=current_user,posts=posts, post_count=post_count,followers_count=followers_count,following_count=following_count)

@views.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password= request.form.get('password')
        cpassword = request.form.get('cpassword')
        profile_image=request.files['pimage']
        userem = User.query.filter_by(email=email).first()
        usernm = User.query.filter_by(username=username).first()
        if userem:
            flash('Email already exists!', category='error')
            return redirect(url_for('views.register'))
        elif usernm:
            flash('Username must be unique!', category='error')
            return redirect(url_for('views.register'))
        elif password != cpassword:
            flash("Password does not match!", category="error")
            return redirect(url_for('views.register'))
        else:
            hashed_password = generate_password_hash(password,method='sha256')
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            #DIRECORY_PATH = os.getcwd()
            #UPLOAD_FOLDER = DIRECORY_PATH + '/application/static/profileimg/'
            def allowed_file(filename):
                return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            if profile_image and allowed_file(profile_image.filename):
                profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(currenttime + profile_image.filename)))
                profileimgname = currenttime + profile_image.filename
                #profileimgname = currenttime+secure_filename(profile_image.filename)
                #profile_image.save(os.path.join('static/profileimg/', profileimgname))
            else:
                flash("Only png/jpg/jpeg files are allowed!", category="error")
                return redirect(url_for('views.register'))
            user=User(username=username,email=email,profile_image=profileimgname,password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {username}!','success')
            return redirect(url_for('views.login'))
    return render_template("signup.html")

@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        email=request.form.get('email')
        password= request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['usr_name']=user.username
                #session['pimg'] = result['pimg']
                session['u_id'] = user.user_id
                flash('You have been logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
        else:
            flash('Login Unsuccessful. Please check username and password.', category='error')
            return redirect(url_for('views.login'))
    return render_template("login.html",user=current_user)


@views.route("/addblog", methods=["GET", "POST"])
@login_required
def addblog():
    if request.method=="POST":
        #if request.form.get('postsub')=="Save":
            title=request.form.get('postname')
            caption=request.form.get('postdesc')
            blogimg = request.files['postimg']
            added_by = current_user.username
            added_date = datetime.datetime.now()
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            def allowed_file(filename):
                return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            if blogimg.filename == '':
                flash('No file was selected')
                return redirect(request.url)
            if blogimg and allowed_file(blogimg.filename):
                blogimg.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(currenttime + blogimg.filename)))
                blogimgname = currenttime + blogimg.filename
                '''#blogimg.save('/static/blogimg/an.jpg')
                    blogimgname = currenttime+blogimg.filename
                    print(blogimgname)
                    print(os.path.join(app.config['UPLOAD_FOLDER'],blogimgname))
                    blogimg.save(os.path.join("static/blogimg",secure_filename(blogimgname)))'''
            else:
                flash('Invalid image file extension!', category='error')
                return redirect(url_for('views.addblog'))
            new_blog = Post(post_title=title, post_caption=caption, post_image=blogimgname, author=current_user.user_id,posted_by=added_by, posted_date=added_date)
            db.session.add(new_blog)
            db.session.commit()
            flash("New Post Added!", category="success")
            return redirect(url_for('views.addblog'))
    return render_template("addblog.html",user=current_user)

@views.route("/delete-post/<post_id>", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    if not post:
        flash("Post does not exist!", category="error")
        return redirect(url_for('views.homepage'))
    elif current_user.user_id != post.author:
        flash("You do not have permission to delete this post!", category="error")
        return redirect(url_for('views.homepage'))
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Blog deleted.', category="success")
        return redirect(url_for('views.homepage'))

@views.route("/posts/<user_id>", methods=["GET", "POST"])
@login_required
def posts(user_id):
    suser=User.query.filter_by(user_id=user_id).first()
    if not suser:
        flash("No user found with this username!", category="error")
        return redirect(url_for('views.homepage'))
    posts = Post.query.filter_by(author=user_id).order_by((Post.posted_date.desc())).all()
    colors=["#cdd6ff","#ffebcd", "#ffcdcd", "#decdff"]
    i=0
    for item in posts:
        print(type(item.author))
        item.color=colors[i]
        print(type(item))
        i+=1
        if i==4:
            i=0   
    post_count=len(Post.query.filter_by(author=suser.user_id).all())
    followers_count=suser.followed.count()
    following_count= suser.followers.count()
    return render_template("userposts.html", posts=posts, user=current_user, suser=suser, post_count=post_count,followers_count=followers_count,following_count=following_count)

@views.route("/editprofile", methods=["GET", "POST"])
@login_required
def editprofile():
    user_id=request.args.get('userid')
    to_update = User.query.get_or_404(user_id)
    if request.method=="POST":
        user_id=request.args.get('userid')
        to_update = User.query.get_or_404(user_id)
        username=request.form.get('username')
        email=request.form.get('email')
        password= request.form.get('password')
        userem = User.query.filter_by(email=email).first()
        usernm = User.query.filter_by(username=username).first()
        if email != to_update.email:
            if userem:
                flash('Email already exists!', category='error')
                return render_template("editprofile.html",user=current_user, euser=to_update,user_id=user_id)
            else:
                to_update.email=request.form.get('email')
        else:
            to_update.email=request.form.get('email')
        if username != to_update.username:
            if usernm:
                flash('Username must be unique!', category='error')
                return render_template("editprofile.html",user=current_user, euser=to_update,user_id=user_id)
            else:
                to_update.username = request.form.get('username')
        else:
                to_update.username = request.form.get('username')
        if check_password_hash(to_update.password, password):
            new_password = request.form.get('cpassword')
            if new_password!="":
                new_hashed_password = generate_password_hash(new_password,method='sha256')
                to_update.password = new_hashed_password
        else:
            flash("Old password is incorrect!", category="error")
            return render_template("editprofile.html",user=current_user, euser=to_update,user_id=user_id)
        profile_image=request.files['pimage']
        
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        def allowed_file(filename):
            return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        if profile_image.filename == '':
            to_update.profile_image=to_update.profile_image
        elif profile_image and allowed_file(profile_image.filename):
            profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(currenttime + profile_image.filename)))
            to_update.profile_image = currenttime + profile_image.filename
        else:
            flash("Only png/jpg/jpeg files are allowed!", category="error")
            return render_template("editprofile.html",user=current_user, euser=to_update,user_id=user_id)
        db.session.commit()
        flash('Updated successfully!', category='success')
        return redirect(url_for('views.homepage'))
    return render_template("editprofile.html",user=current_user, euser=to_update,user_id=user_id)

@views.route("/editpost", methods=["GET", "POST"])
@login_required
def editpost():
    post_id=request.args.get('postid')
    #euser = User.query.filter_by(username=username).first()
    to_update = Post.query.get_or_404(post_id)
    if request.method=="POST":
        post_id=request.args.get('postid')
        to_update = Post.query.get_or_404(post_id)
        to_update.post_title=request.form.get('postname')
        to_update.post_caption=request.form.get('postdesc')
        blogimg = request.files['postimg']
        to_update.posted_by = current_user.username
        to_update.author = current_user.user_id
        to_update.updated_date = datetime.datetime.now()
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        def allowed_file(filename):
            return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        if blogimg.filename == '':
            flash('No file was selected')
            return redirect(request.url)
        if blogimg and allowed_file(blogimg.filename):
            blogimg.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(currenttime + blogimg.filename)))
            to_update.post_image = currenttime + blogimg.filename
        db.session.commit()
        flash('Updated successfully!', category='success')
        return redirect(url_for('views.homepage'))
    return render_template("editpost.html",user=current_user,epost=to_update,post_id=post_id)

@views.route("/deleteuser", methods=["GET", "POST"])
@login_required
def deleteuser():
    user_id=request.args.get('userid')
    user = User.query.filter_by(user_id=user_id).first()
    #posts=Post.query.filter_by(author=user_id).all()
    if not user:
        flash("User does not exist!", category="error")
        return redirect(url_for('views.homepage'))
    elif current_user.user_id != user.user_id:
        flash("You do not have permission to delete this account!", category="error")
        return redirect(url_for('views.homepage'))
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Account deleted!', category="success")
        return redirect(url_for('views.register'))

@views.route('/comments/<post_id>', methods=["GET", "POST"])
@login_required
def comments(post_id):
    if request.method=="POST":
        comment = request.form.get('comment')
        added_date=datetime.datetime.now()
        post=Post.query.filter_by(post_id=post_id).first()
        if post:
            comment=Comment(comment=comment, added_date=added_date, author=current_user.user_id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('views.homepage'))
    #comments = Comment.query.order_by(Comment.id.desc()).all()
    #return render_template('comments.html', comments=comments,user=current_user)

@views.route('/delete-comment/<int:comment_id>', methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category="error")
    elif current_user.user_id != comment.author:
        flash('You do not have permission to delete this post!', category="error")
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('views.homepage'))

@views.route('/like/<int:post_id>', methods=["GET", "POST"])
@login_required
def like(post_id):
    post=Post.query.filter_by(post_id=post_id).first()
    like = Like.query.filter_by(author=current_user.user_id, post_id=post_id).first()
    if not post:
        flash("Post does not exist!", category="error")
        return redirect(url_for('views.homepage'))
    elif like:
        db.session.delete(like)
        db.session.commit()
        return redirect(url_for('views.homepage'))
    else:
        like=Like(author=current_user.user_id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return redirect(url_for('views.homepage'))


@views.route('/follow/<username>', methods=['GET','POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User not found.')
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('views.posts', user_id=user.user_id))
    current_user.follow(user)
    db.session.commit()
    flash(f'{username} followed!', category="success")
    return redirect(url_for('views.posts', user_id=user.user_id))

@views.route('/unfollow/<username>', methods=['GET','POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found.')
        return redirect(url_for('views.homepage'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('views.posts', user_id=user.user_id))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'Unfollowed {username}!', category='error')
    return redirect(url_for('views.posts', user_id=user.user_id))


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))