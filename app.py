from flask import Flask, request, redirect, render_template, session, url_for, flash
import os
import re
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# In-memory storage for demonstration purposes
text_storage = {}

def generate_unique_id():
    # Generate a random string of 6 letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def convert_urls_to_links(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    def replace_with_link(match):
        url = match.group(0)
        return f'<a href="{url}">{url}</a>'
    return url_pattern.sub(replace_with_link, text)

def valid_login(username, password):
    return username == "admin" and password == "password"

def is_user_logged_in():
    return 'user_id' in session

@app.route('/', methods=['GET', 'POST'])
def home():
    logged_in = is_user_logged_in()
    return render_template('index.html', logged_in=logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            session['user_id'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
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
    submitted_text = request.form['text']
    linked_text = convert_urls_to_links(submitted_text)
    unique_id = generate_unique_id()  # Generate a unique 6-character ID
    text_storage[unique_id] = linked_text  # Store the text with its unique ID
    # Redirect to a URL that includes the unique ID
    return redirect(url_for('view_text', text_id=unique_id))

@app.route('/text/<text_id>')
def view_text(text_id):
    text = text_storage.get(text_id, "Text not found.")  # Retrieve the text by its unique ID
    # Use the display_text.html template to render the text
    return render_template('display_text.html', text=text)

@app.route('/my_links', methods=['GET'])
def my_links():
    if not is_user_logged_in():
        return redirect(url_for('login'))
    links = ['Link1', 'Link2', 'Link3']
    return render_template('my_links.html', links=links)

#if __name__ == '__main__':
    #app.run(host='localhost', port=8080, debug=True)


