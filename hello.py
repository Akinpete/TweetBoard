"""
app.py - Main entry point for the Flask web application.

This application provides functionalities for managing posts,
including creating, deleting, and displaying posts.
"""

from flask import Flask, redirect, render_template, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user,current_user
from flask_migrate import Migrate
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity, JWTManager
)
from flask_cors import CORS
from get_token import get_token
from form_url import build_url, get_tweet_data
from tweet_type import tweet_type, safe_get_video_url
from markupsafe import Markup
# GET RAW SQL for monitoring in console
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy').setLevel(logging.INFO)


# Create a Flask Instance
app = Flask(__name__)

# Configure Flask App
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://peter_dev:peter_dev_pwd@localhost/test_bookmarks_db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Example: 1 hour
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Example: 30 days

#Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app,db)
jwt = JWTManager(app)
CORS(app)

@app.template_filter('nl2br')
def nl2br_filter(s):
    return Markup(s.replace('\n', '<br>\n'))

# Flask Login SetUp
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


#Extension
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Get new access token from the refresh token.

    When access token expires, it generates new access token
    for the user to be authenticated. 
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200


# Extension route
@app.route('/login/extension', methods=['POST'])
def login_extension():
    """
    Backend logic for chrome extension auth

    Receives POST request from chrome extension
    background worker and process the auth,
    then send appropriate response
    """
    username = request.json.get('username')
    password = request.json.get('password')
    user=Users.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password_hash, password):
            # login_user(user)            
            access_token = create_access_token(identity={'username': user.username})
            refresh_token = create_refresh_token(identity={'username': user.username})
            return jsonify(access_token=access_token, refresh_token=refresh_token), 200
        else:
            return jsonify({'msg': 'Incorrect password!'})     
    return jsonify({'msg': 'User does not exist!'}), 401

@app.route('/delete/one/<int:id>', methods=['GET'])
@login_required
def delete_post(id):
    """
    Delete a post by its ID.

    Retrieves the post from the database using the given ID.
    If the post exists, it is deleted; otherwise, a 'Post Not Found' message is shown.
    Redirects to the bookmarks page after deletion.
    """
    post_id = id
    post = Posts.query.filter_by(id=post_id).first()
    if not post:
        flash("Post Not Found")
        return redirect(url_for('get_bookmark'))
    
    db.session.delete(post)
    db.session.commit()
    flash("Post successfully deleted")
    return redirect(url_for('get_bookmarks')) 
    

@app.route('/bookmark/one/<int:id>', methods=['GET'])
@login_required
def get_bookmark(id):
    """
    Display a post by its ID.

    Retrieves the post from the database using the given ID.
    If the post exists, it is shown; otherwise, a 'Post Not Found' message is shown.
    
    """
    post_id = id
    post = Posts.query.filter_by(id=post_id).first()
    if not post:
        flash("Post Not Found")
        
    details = {
            "pfp_link": post.pfp_link,
            "type_tweet": post.type_tweet,            
            "tweet_text": post.tweet_text,
            "bold_name": post.bold_name,
            "at_name": post.at_name,
            "image_link": post.image_link,
            "video_link": post.video_link,
            "id": post.id,
            "tweet_link": post.tweet_link          
        }
    
    return render_template('bookmark.html', details=details)  

@app.route('/bookmark/all', methods=['GET'])
@login_required
def get_bookmarks():
    """
    Display all bookmarks for the current user.

    This route is protected by login_required, allowing access only to authenticated users.
    It retrieves the current user's posts and prepares a list of tweet details, including 
    profile picture link, tweet type, truncated tweet text (up to 80 characters), full tweet 
    text, bold name, @name, image link, video link, and post ID.

    The prepared tweet details are rendered in the 'bookmarks_copy.html' template.
    """
    user_id = current_user.id
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        flash("User Not found!")
    tweet_details = []
    posts = user.posts
    for post in posts:
        if post.tweet_text:
            if len(post.tweet_text) > 80:        
                shortened_text = post.tweet_text[:80]
            else:
                shortened_text = None
        details = {
            "pfp_link": post.pfp_link,
            "type_tweet": post.type_tweet,
            "tweet_text1": shortened_text,
            "tweet_text2": post.tweet_text,
            "bold_name": post.bold_name,
            "at_name": post.at_name,
            "image_link": post.image_link,
            "video_link": post.video_link,
            "id": post.id          
        }
        
        tweet_details.append(details) 

    
    return render_template('bookmarks_copy.html', tweet_details=tweet_details)
# Protected route to add bookmark
@app.route('/bookmark', methods=['POST'])
@jwt_required()
def add_post():
    """
    Receives bookmark id from chrome extension,
    processes it and extracts the details from API,
    add it to database  
 
    """
    # Debugging: Print received headers
    print("Received headers:", request.headers)
    
    data = request.get_json()
    print("Received data:", data)
    
    tweet_id = data.get('tweet_id')
    if not tweet_id:
        return jsonify({'msg': 'Tweet ID is required'}), 400
    
    claims = get_jwt_identity()
    print("JWT Claims:", claims)
    
    username = claims['username']
    
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404
       
    check = tweet_type(tweet_id)
    
    pfp_link = check.get("profile_image_url")
    type_tweet = check.get("type")
    tweet_text = check.get("text")
    bold_name = check.get("name")
    at_name = check.get("screen_name")
    tweet_link = "https://x.com/{}/status/{}".format(at_name, tweet_id)
    image_link = check.get("image_url")    
    video_link = safe_get_video_url(check.get("video_variants"))
    tweet_link = tweet_link
    
    
    new_bookmark = Posts(tweet_id=tweet_id, poster_id=user.id, pfp_link=pfp_link,tweet_text=tweet_text,
                         bold_name=bold_name,at_name=at_name,image_link=image_link, video_link=video_link, type_tweet=type_tweet,tweet_link=tweet_link)
    db.session.add(new_bookmark)
    db.session.commit()   
    
    return jsonify({'msg': 'Bookmark added to db'}), 201



# Create a route decorator
@app.route('/')
def index():
    """
    Renders the home page
        
    """ 
    if current_user.is_authenticated:
        flash("You're already Logged in!")
        return redirect(url_for('get_bookmarks'))   
    # flash("Welcome to Our Website!")    
    return render_template('index.html')

@app.route('/about')
def about():
    """
    Renders the about page
        
    """ 
    return render_template('about.html')



@app.route('/dashboard')
@login_required
def dashboard():
    """
    Renders the dashboard for each user page
        
    """ 
#     id=current_user.id
#     user=
    
    return render_template('dashboard.html')
 
# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    Renders the dashboard for each user page
        
    """ 
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('login'))
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    Renders the login form on GET requests and processes the login on POST requests. 
    If the credentials are valid, the user is logged in and redirected to the homepage.
    Otherwise, an error message is flashed, and the login form is re-displayed.
    """
    form = LoginForm()
    logged_in = None
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                logged_in = True
                flash("Login Successful!!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("User doesn't exist! Try again")
    return render_template('login.html',form=form, logged_in=logged_in)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    Displays the registration form on GET requests and processes user registration on POST requests.
    If the registration is successful, the new user is added to the database, and a success message is flashed.
    The user is then redirected to the login page. If there are errors, an error message is flashed, and the 
    registration form is re-displayed.
    """
    form = UserForm()
    username = None
    our_users = Users.query.order_by(Users.date_added)
    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(email=form.email.data).first()
            if user:
                flash("Email already registered. Please use a different email.")
            else:
                hashed_pw = generate_password_hash(form.password_hash.data, method="pbkdf2:sha256")
                user=Users(name=form.name.data, username=form.username.data,
                           email=form.email.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
                flash("User Added successfully")
                return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash("Username or Email already exists. Please use different details.")
        except Exception as e:
            # Handle other exceptions
            db.session.rollback()
            flash("An error occurred while adding the user.")
            print(f"Error: {e}")
            
        username = form.username.data
        form.name.data = ""
        form.username.data = ""        
        form.email.data = ""        
        form.password_hash.data = ""             
    
    return render_template('register.html', form=form, 
                           username=username, our_users=our_users)
    
class LoginForm(FlaskForm):
    """
    Form for handling user login.

    Contains fields for entering a username and password, each with a DataRequired validator to ensure 
    that the fields are not left empty. Also includes a submit button to submit the form.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    """
    Form for handling user registration.

    Contains fields for entering a username, email, and password, each with a DataRequired validator 
    to ensure that the fields are not left empty. Also includes a submit button to submit the form.
    """
    name = StringField("Full Name", validators=[DataRequired()])
    username = StringField("Username, might be/not be your X username", validators=[DataRequired(), Length(max=49)])    
    email = StringField("Email", validators=[DataRequired(), Email(message='Please Input a Valid Email')])    
    password_hash = PasswordField('Password', validators=[DataRequired()])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_hash', message='passwords must match')])
    submit = SubmitField("Submit")
    
class Users(db.Model, UserMixin):
    """
    Represents a user in the application.

    Attributes:
    - id: Primary key for the user.
    - username: Unique username for the user.
    - name: Full name of the user.
    - email: Unique email address of the user.
    - date_added: Timestamp when the user was added, defaults to current time.
    - password_hash: Hashed password for the user.
    - posts: Relationship to associate the user with their posts.

    Methods:
    - password (property): Raises an error when trying to read the password.
    - password (setter): Hashes and sets the user's password.
    - verify_password: Checks if a given password matches the stored hash.
    - __repr__: Returns a string representation of the user by name.
    """
    id=db.Column(db.Integer, primary_key=True)  
    username=db.Column(db.String(50), nullable=False, unique=True)  
    name=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(120), nullable=False, unique=True)    
    date_added=db.Column(db.DateTime, default=datetime.utcnow)
    password_hash=db.Column(db.String(128))
    #User can have many posts
    posts = db.relationship('Posts', backref='poster')
    
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
#Create a Blog Post Model
class Posts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    tweet_id=db.Column(db.String(100))
    date_posted=db.Column(db.DateTime, default=datetime.utcnow)
    type_tweet = db.Column(db.String(10), nullable = False)
    pfp_link = db.Column(db.Text, nullable=False)
    video_link=db.Column(db.Text, nullable=True)
    image_link=db.Column(db.Text, nullable=True)
    tweet_text=db.Column(db.Text, nullable=False)
    bold_name=db.Column(db.String(50), nullable=False )
    at_name=db.Column(db.String(50), nullable=False)
    tweet_link=db.Column(db.Text, nullable=False)
    # Foreign Key to refer to Primary Key of the user
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Association table foreign key
    tags = db.relationship('Tags', secondary = 'post_tags', back_populates = 'posts')

#Create a Tag db Model
class Tags(db.Model):
    """
    Represents a bookmarked tweet.

    Attributes:
    - id: Primary key for the post.
    - tweet_id: Identifier for the tweet associated with the post.
    - date_posted: Timestamp when the post was created, defaults to current time.
    - type_tweet: Type of tweet (e.g., original, retweet).
    - pfp_link: URL link to the profile picture.
    - video_link: URL link to an associated video (optional).
    - image_link: URL link to an associated image (optional).
    - tweet_text: Text content of the tweet.
    - bold_name: Display name of the user who posted.
    - at_name: @username of the user who posted.
    - tweet_link: URL link to the tweet.
    - poster_id: Foreign key linking to the user who posted.
    - tags: Relationship to associate the post with multiple tags.
    """
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Association table foreign key
    posts = db.relationship('Posts', secondary = 'post_tags', back_populates = 'tags')

#Associative table itself for the many-to-many relationship.    
class PostTags(db.Model):
    """
    Associative table for the many-to-many relationship between Posts and Tags.

    Attributes:
    - post_id: Foreign key referencing the primary key of a post.
    - tag_id: Foreign key referencing the primary key of a tag.

    This table establishes the connection between posts and tags, enabling each post 
    to be associated with multiple tags and vice versa.
    """
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)