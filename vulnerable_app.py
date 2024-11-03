from flask import Flask, request, render_template_string

app = Flask(__name__)

# User settings page with a form to change settings
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Vulnerable: No CSRF protection
        new_setting = request.form.get('setting')
        return f"Settings have been updated to: {new_setting}"
    return render_template_string('''
        <form method="post" action="/settings">
            <label for="setting">Change Setting:</label>
            <input type="text" name="setting" id="setting">
            <input type="submit" value="Update">
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
