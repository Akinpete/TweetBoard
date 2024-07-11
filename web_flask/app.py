from flask import Flask, render_template, flash, url_for, redirect
from models import storage
from models.user import User
from .forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.config['SECRET_KEY'] = 'akinpete'

# Initialize CSRF protection
csrf = CSRFProtect(app)

@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()
    
    
@app.route("/" , strict_slashes = False)
def index():
    return "Hello HBNB!"

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')        
        new_user = User(email=form.email.data, username=form.username.data)
        new_user.set_password(form.password.data) 
        storage.new(new_user)
        storage.save()
        
        return redirect(url_for('index'))    
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()    
    return render_template('login.html', title='Login', form=form)



    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)