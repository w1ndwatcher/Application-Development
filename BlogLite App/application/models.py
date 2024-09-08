from . import db
import datetime
from flask_login import UserMixin

# auxiliary table
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'))
)

class User(db.Model,UserMixin):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    profile_image = db.Column(db.String)
    password = db.Column(db.String, unique=True)
    posts = db.relationship('Post', backref='user', passive_deletes=True,cascade="all,delete")
    comments = db.relationship('Comment', backref='user', passive_deletes=True,cascade="all,delete")
    likes = db.relationship('Like', backref='user', passive_deletes=True,cascade="all,delete")
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == user_id), secondaryjoin=(followers.c.followed_id == user_id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic',passive_deletes=True,cascade="all,delete")
    def get_id(self):
        return (self.user_id)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.user_id).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.author)).filter(
            followers.c.follower_id == self.user_id)
        own = Post.query.filter_by(author=self.user_id)
        return followed.union(own).order_by(Post.posted_date.desc())

class Post(db.Model):
    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_title = db.Column(db.String(100))
    post_caption = db.Column(db.Text)
    post_image = db.Column(db.String)
    posted_by = db.Column(db.String)
    #color=db.Column(db.String)
    posted_date = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_date = db.Column(db.DateTime, onupdate=datetime.datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True,cascade="all,delete")
    likes = db.relationship('Like', backref='post', passive_deletes=True,cascade="all,delete")

class Comment(db.Model):
    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.String(250))
    added_date = db.Column(db.DateTime, default=datetime.datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete="CASCADE"), nullable=False)

class Like(db.Model):
    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    added_date = db.Column(db.DateTime, default=datetime.datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete="CASCADE"), nullable=False)



