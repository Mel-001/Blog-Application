from . import main
from flask_login import login_required,current_user
from flask import render_template,redirect,url_for,abort,request,flash
from ..models import User,Blog,Comment,Subscriber
from .. import db,photos
from ..request import get_quotes
from .forms import BlogForm, CommentForm,UpdateProfile,SubscribeForm
from ..email import mail_message
import markdown2 

#Views
@main.route('/', methods = ['GET','POST'])
def index():
    '''
    view to load index.html
    '''

    quote = get_quotes()
    
    blogs = Blog.query.all()
    
  

    return render_template('index.html',quote = quote, blogs = blogs)
    

@main.route('/user/<usersname>')
def profile(usersname):
    user = User.query.filter_by(username = usersname).first()
    user_joined = user.date_joined.strftime('%b %d, %Y')


    if user is None:
        abort(404)
        

    

    return render_template("profile/profile.html", user = user, date = user_joined)

@main.route('/blog/new', methods = ['GET','POST'])
@login_required
def new_blog():
    
    subscribers = Subscriber.query.all()
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        blog_title = blog_form.blog_title.data
        blog_content = blog_form.blog_content.data
        
    
        # Updated blog instance
        new_blog = Blog(blog_title = blog_title, blog_content=blog_content,user=current_user)

        # Save blog method
        new_blog.save_blog()
        for subscriber in subscribers:
            mail_message("Alert New Blog","email/new_blog",subscriber.email,new_blog=new_blog)
        return redirect(url_for('.index'))

    
    return render_template('newblog.html',blog_form = blog_form )

@main.route('/blog/<id>', methods = ['GET','POST'])
def blogs(id):

    '''
    View root page function that returns the blog page and its data
    '''

    blogs = Blog.query.filter_by(id=id).first()
    blog = Blog.query.filter_by(id=blogs.id).first()
    blog_id = blog.id
    comments = Comment.get_comments(blog)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = comment_form.text.data
        new_comment = Comment(comment = comment,user = current_user, blog = blog_id)
        new_comment.save_comment()
        
        flash('Your comment has been submitted')
    
    
    return render_template('blog.html', blogs = blogs, comment_form = comment_form, comments = comments)


@main.route('/user/<usersname>/update',methods = ['GET','POST'])
@login_required
def update_profile(usersname):
    user = User.query.filter_by(username = usersname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',usersname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<usersname>/update/pic',methods= ['POST'])
@login_required
def update_pic(usersname):
    user = User.query.filter_by(username = usersname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',usersname=usersname))

@main.route('/subscribe/', methods=['GET','POST'])
def subscriber():
    subscribe_form=SubscribeForm()

    if subscribe_form.validate_on_submit():

        subscriber= Subscriber(email=subscribe_form.email.data,name = subscribe_form.name.data)

        db.session.add(subscriber)
        db.session.commit()

        mail_message("Welcome to K-Blogs","email/subscriber",subscriber.email,subscriber=subscriber)

    subscriber = Blog.query.all()

    blog = Blog.query.all()


    return render_template('subscribe.html',subscriber=subscriber,subscribe_form=subscribe_form,blog=blog)