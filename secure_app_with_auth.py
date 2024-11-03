from flask import Flask, request, render_template_string, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging

# Setup Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Setup logging
logging.basicConfig(level=logging.INFO)

# User model with roles
class User(UserMixin):
    def __init__(self, id, role='user'):
        self.id = id
        self.role = role

# Mock user database with roles
users = {
    'admin': {'password': 'password', 'role': 'admin'},
    'user': {'password': 'userpass', 'role': 'user'}
}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id, role=users.get(user_id, {}).get('role', 'user'))

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

# Settings form
class SettingsForm(FlaskForm):
    setting = StringField('Change Setting:')
    submit = SubmitField('Update')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            user = User(username, role=users[username]['role'])
            login_user(user)
            logging.info(f"User {username} logged in successfully.")
            return redirect(url_for('settings'))
        else:
            logging.warning(f"Failed login attempt for user {username}.")
    return render_template_string('''
        <form method="post" action="/login">
            {{ form.hidden_tag() }}
            {{ form.username.label }} {{ form.username() }}<br>
            {{ form.password.label }} {{ form.password() }}<br>
            {{ form.submit() }}
        </form>
    ''', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logging.info(f"User {current_user.id} logged out.")
    logout_user()
    return redirect(url_for('login'))

# Settings route with CSRF protection
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        new_setting = form.setting.data
        logging.info(f"User {current_user.id} updated setting to: {new_setting}")
        return f"Settings have been updated to: {new_setting}"
    return render_template_string('''
        <form method="post" action="/settings">
            {{ form.hidden_tag() }}
            {{ form.setting.label }} {{ form.setting() }}
            {{ form.submit() }}
        </form>
        <a href="{{ url_for('logout') }}">Logout</a>
    ''', form=form)

# Admin route with access control
@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.role != 'admin':
        logging.warning(f"User {current_user.id} attempted to access admin page without permission.")
        return "Access denied", 403
    logging.info(f"Admin page accessed by user {current_user.id}.")
    return "Welcome to the admin page!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
