from flask import Flask, render_template_string, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="bookstore_db"
    )

index_html = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Bookstore Home</title></head><body><h1>Welcome to The Book Imperium</h1><nav><a href='{{ url_for('view_books') }}'>View Books</a> | <a href='{{ url_for('add_book') }}'>Add Book</a></nav></body></html>"""

books_html = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Books List</title></head><body><h1>Books Available</h1><ul>{% for book in books %}<li>{{ book['name'] }} - {{ book['category'] }} - ${{ book['price'] }}</li>{% endfor %}</ul><a href="/">Back to Home</a></body></html>"""

add_book_html = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Add a New Book</title></head><body><h1>Add a New Book</h1><form method="POST" action="{{ url_for('add_book') }}"><label for="book_name">Book Name:</label><input type="text" id="book_name" name="book_name" required><br><label for="category">Category:</label><input type="text" id="category" name="category" required><br><label for="price">Price:</label><input type="number" step="0.01" id="price" name="price" required><br><button type="submit">Add Book</button></form><a href="/">Back to Home</a></body></html>"""

@app.route('/')
def home():
    return render_template_string(index_html)

@app.route('/books')
def view_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template_string(books_html, books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        category = request.form['category']
        price = request.form['price']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (name, category, price) VALUES (%s, %s, %s)", (book_name, category, price))
        conn.commit()
        conn.close()
        flash('Book added successfully!')
        return redirect(url_for('view_books'))
    return render_template_string(add_book_html)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
