from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager


class User(UserMixin,db.Model):
  __tablename__ = 'users'
  id =db.Column(db.Integer,primary_key =True)
  username = db.Column(db.String(255),index = True)
  firstname = db.Column(db.String(255))
  lastname = db.Column(db.String(255))
  email = db.Column(db.String(255),unique = True,index = True)
  bio = db.Column(db.String(1000))
  profile_pic_path = db.Column(db.String)
  pass_secure = db.Column(db.String(255))
  date_joined = db.Column(db.DateTime,default=datetime.utcnow)
  blogs = db.relationship('Blog',backref = 'user',lazy = "dynamic")
  comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")



  @property
  def password(self):
    raise AttributeError('The password is private')

  @password.setter
  def password(self,password):
    self.pass_secure = generate_password_hash(password)

  def verify_password(self,password):
    return check_password_hash(self.pass_secure,password)


  def __repr__(self):
    return f'User {self.username}'

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
  '''
    Quote class to define Quotes Objects
      
  '''
  def __init__(self,id,author,quote,permalink):
        self.id =id
        self.author = author
        self.quote = quote
        self.permalink = permalink

class Blog(db.Model):
  __tablename__ = "blogs"

  id = db.Column(db.Integer,primary_key = True)
  blog_title = db.Column(db.String(255))
  blog_content = db.Column(db.String)
  user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  comments = db.relationship('Comment',backref =  'blog_id',lazy = "dynamic")

  def save_blog(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_blogs(cls,category):
    blogs = Blog.query.filter_by(category=category).all()
    return blogs

  @classmethod
  def get_blog(cls,id):
    blog = Blog.query.filter_by(id=id).last()

    return blog

class Comment(db.Model):

  __tablename__ = 'comments'
  id = db.Column(db.Integer,primary_key = True)
  comment = db.Column(db.String(500))
  user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
  blog = db.Column(db.Integer,db.ForeignKey("blogs.id"))

  

  def save_comment(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_comments(cls,blog):
    comments = Comment.query.filter_by(blog_id=blog).all()
    return comments
        
class Subscriber(UserMixin, db.Model):
   __tablename__="subscribers"

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255))
   email = db.Column(db.String(255),unique = True,index = True)


   def save_subscriber(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def get_subscribers(cls,id):
       return Subscriber.query.all()


   def __repr__(self):
       return f'User {self.email}'
   