from flask import Flask, request, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

class SettingsForm(FlaskForm):
    setting = StringField('Change Setting:')
    submit = SubmitField('Update')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        new_setting = form.setting.data
        return f"Settings have been updated to: {new_setting}"
    return render_template_string('''
        <form method="post" action="/settings">
            {{ form.hidden_tag() }}
            {{ form.setting.label }} {{ form.setting() }}
            {{ form.submit() }}
        </form>
    ''', form=form)

if __name__ == '__main__':
    app.run(debug=True)
