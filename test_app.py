import pytest
from app import app
from db import Database
from app import teardown_appcontext
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db():
    return Database(db_name='test_books', mongo_uri="mongodb://localhost:27017/test_books")

def test_login(client):
    response = client.get('/')
    assert b'<form method="post">' in response.data

def test_dashboard(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert b'login' in response.data


def test_add_book(client):
    response = client.get('/add')
    assert b'<h1>Add Book</h1>' in response.data
    assert b'<form method="POST">' in response.data
    assert b'<label for="title">Title:</label>' in response.data
    assert b'<input type="text" id="title" name="title" required>' in response.data
    assert b'<label for="author">Author:</label>' in response.data
    assert b'<input type="text" id="author" name="author" required>' in response.data
    assert b'<label for="year">Year:</label>' in response.data
    assert b'<input type="text" id="year" name="year" required>' in response.data
    assert b'<button type="submit">Add Book</button>' in response.data

def test_delete_books_no_books(client):
    # Simulate login process
    client.post('/', data={'username': 'test_user', 'password': 'password'}, follow_redirects=True)
    
    # Mock the database query to return an empty list of books
    with patch('app.client') as mock_client:
        mock_collection = mock_client.__getitem__.return_value.__getitem__.return_value
        mock_collection.find.return_value = []

        # Access the delete books page
        delete_books_response = client.get('/delete', follow_redirects=True)

        # Check if the message is present in the response data
        assert b'No books found in your collection.' in delete_books_response.data


def test_edit_books(client):
    # Simulate login process
    login_response = client.post('/', data={'username': 'test_user', 'password': 'password'}, follow_redirects=True)
    assert b'Welcome' in login_response.data  # Assert that the user is redirected to the dashboard after login

    # Access the edit books page after login
    edit_books_response = client.get('/edit', follow_redirects=True)
    assert edit_books_response.status_code == 200  # Check if the edit books page is accessed successfully

    # Press the button to edit a book
    edit_book_response = client.post('/edit', data={'selected_book': 'book_title', 'title': 'New Title', 'author': 'New Author', 'year': '2024'}, follow_redirects=True)
    assert edit_book_response.status_code == 200  # Check if the user is redirected to the dashboard page
    assert b'Welcome test_user' in edit_book_response.data  # Check if the welcome message with the username is present
    assert b'Add Book' in edit_book_response.data  # Check if the button to add a book is present (indicating the dashboard page)
    assert b'Delete Book' in edit_book_response.data  # Check if the button to delete a book is present
    assert b'Edit Book' in edit_book_response.data  # Check if the button to edit a book is present
    assert b'Show Books' in edit_book_response.data  # Check if the button to show books is present


def test_show_books(client):
    # Simulate login process
    login_response = client.post('/', data={'username': 'test_user', 'password': 'password'}, follow_redirects=True)
    assert b'Welcome' in login_response.data  # Assert that the user is redirected to the dashboard after login

    # Access the dashboard page after login
    dashboard_response = client.get('/dashboard', follow_redirects=True)
    assert b'Welcome test_user' in dashboard_response.data  # Ensure the dashboard page contains the welcome message

    # Click the "Show Books" button on the dashboard
    show_books_link = '/show_books'
    show_books_response = client.get(show_books_link, follow_redirects=True)
    assert show_books_response.status_code == 200  # Check if the response status code is 200
    assert b'Your Books' in show_books_response.data  # Check if the response contains the expected content
    assert b'Back to Dashboard' in show_books_response.data  # Check if the response contains the link back to the dashboard

def test_teardown_appcontext():
    # Create a mock MongoDB client
    mock_client = MagicMock()

    # Assign the mock client to the database client attribute in the app module
    with patch('app.db.client', mock_client):
        # Call the teardown function
        teardown_appcontext()

        # Assert that the close method of the mock client is called once
        mock_client.close.assert_called_once()

