from flask import Flask, request, redirect, render_template, session, url_for , flash
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Function to convert URLs in text to clickable links
def convert_urls_to_links(text):
    # Regular expression to match URLs
    url_pattern = re.compile(r'(https?://[^\s]+)')
    # Function to wrap matched URLs in <a> tags
    def replace_with_link(match):
        url = match.group(0)
        return f'<a href="{url}">{url}</a>'
    # Replace all URLs in the text with <a> tags
    return url_pattern.sub(replace_with_link, text)

# Dummy function to simulate user login validation
def valid_login(username, password):
    # Replace with actual validation logic, and use hashed passwords in production
    return username == "admin" and password == "password"

# Function to check if a user is logged in
def is_user_logged_in():
    return 'user_id' in session

@app.route('/', methods=['GET', 'POST'])
def home():
    logged_in = is_user_logged_in()
    return render_template('index.html', logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            session['user_id'] = username  # Secure session management
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', message=message)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Securely log out the user
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the registration logic here
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/display_text', methods=['POST'])
def display_text():
    # Get the text submitted from the form
    submitted_text = request.form['text']
    linked_text = convert_urls_to_links(submitted_text)  # Convert any URLs in the text to clickable links
    # Render the display_text.html template, passing in the processed text
    return render_template('display_text.html', text=linked_text)

@app.route('/my_links', methods=['GET'])
def my_links():
    if not is_user_logged_in():
        return redirect(url_for('login'))
    links = ['Link1', 'Link2', 'Link3']  # Simulate fetching user's links
    return render_template('my_links.html', links=links)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
