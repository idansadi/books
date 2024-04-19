from flask import Flask, request, session, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
from db import Database  # Import Database class from db.py
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
metrics = PrometheusMetrics(app)

# Define MongoDB URI
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb.default.svc.cluster.local:27017/books")

client = MongoClient(mongo_uri)

# Initialize Database instance
db = Database(db_name='books', mongo_uri=mongo_uri)
# Function to get or create user's collection based on username
def get_user_collection(username):
    return db.get_user_collection(username)


# Function to create a new collection for the user
def create_user_collection(username):
    user_collection_name = f'user_{username}'
    if user_collection_name not in client.list_database_names():
        client[f'user_{username}']  # Create the collection
        print(f"Collection '{user_collection_name}' created for user '{username}'")

# Function to get or create user's collection based on username
def get_user_collection(username):
    create_user_collection(username)
    return client[f'user_{username}']

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Here you can perform authentication, e.g., check username/password against a database
        # For simplicity, we'll just set a session variable to store the username
        session['username'] = username
        print(f'Logged in as {username}')
        return redirect(url_for('dashboard'))
    print("Rendering login.html template")
    return render_template('login.html')  # Render the login.html template

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=username)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Handle the form submission to add a book
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))

        # Retrieve form data
        title = request.form.get('title')
        author = request.form.get('author')
        year_str = request.form.get('year')

        if year_str:
            try:
                year = int(year_str)
            except ValueError:
                return 'Invalid year format. Please enter a valid year.'
        else:
            return 'Year field is required.'

        # Perform further processing (e.g., saving to MongoDB)
        user_db = client['books']  # Assuming the name of the database is 'books'
        user_collection = user_db[f'user_{username}']
        book = {"title": title, "author": author, "year": year}
        user_collection.insert_one(book)

        # Redirect the user back to the dashboard
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        # Render the form to add a book
        return render_template('add_book.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_books():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user_db = client['books']  # Assuming the name of the database is 'books'
    user_collection = user_db[f'user_{username}']

    if request.method == 'POST':
        selected_titles = request.form.getlist('selected_books')
        for title in selected_titles:
            user_collection.delete_one({'title': title})
        return redirect(url_for('dashboard'))

    books = list(user_collection.find())

    # Check if books exist in the collection
    if books:
        return render_template('delete_books.html', books=books)
    else:
        return render_template('delete_books.html', message="No books found in your collection.")


@app.route('/edit', methods=['GET', 'POST'])
def edit_books():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user_db = client['books']
    user_collection = user_db[f'user_{username}']

    if request.method == 'POST':
        selected_book_title = request.form.get('selected_book')
        new_title = request.form.get('title')
        new_author = request.form.get('author')
        new_year = request.form.get('year')

        # Update the selected book in the database with the new values
        user_collection.update_one(
            {'title': selected_book_title},
            {'$set': {'title': new_title, 'author': new_author, 'year': new_year}}
        )

        # Redirect the user back to the dashboard page
        return redirect(url_for('dashboard'))

    # Retrieve all books from the collection
    books = list(user_collection.find())

    return render_template('edit_book.html', books=books)



@app.route('/show_books')
def show_books():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Retrieve all books from the collection
    books = db.get_books(username)

    if not books:
        return render_template('show_books.html', message="No books found in your collection.")

    return render_template('show_books.html', books=books)


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    # Close MongoDB client at the end of the application context
    db.client.close()
    print("Database connection closed")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
