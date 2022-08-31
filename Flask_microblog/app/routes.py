# from app import app

# Home page route.
# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"


# Home page route with HTML added. 
# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'username': 'Miguel'}
#     return '''
# <html>
#     <head>
#         <title>Home Page - Microblog</title>
#     </head>
#     <body>
#         <h1>Hello, ''' + user['username'] + '''!</h1>
#     </body>
# </html>'''

from flask import render_template
from app import app

# # Homepage with templated HTML for adding dynamic behavior and separation of logic from presentation.
# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'username': 'Caleb Bowyer'}
# #     return render_template('index.html', user=user)
#     return render_template('index.html', title='Home', user=user)


# Homepage with templated HTML and passing in posts: 
from flask_login import login_required
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Caleb Bowyer'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    # return render_template('index.html', title='Home', user=user, posts=posts)
    return render_template("index.html", title='Home Page', posts=posts)


from app.forms import LoginForm

# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Sign In', form=form)

from flask import flash, redirect, url_for

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)


from flask_login import current_user, login_user
from app.models import User

from flask import request
from werkzeug.urls import url_parse


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('index'))
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    
    return render_template('login.html', title='Sign In', form=form)


from flask_login import logout_user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

from app.forms import RegistrationForm
# User registration view function: 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User profile view function:
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



