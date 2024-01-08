from flask import Flask , session , request , jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasebooksandscrolls.db'  
# Use SQLite database named 'databasebooksandscrolls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Defining the Books Table
class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30))
    description = db.Column(db.String(300))
    year_published = db.Column(db.Integer, CheckConstraint('length(year_published) = 4'))
    book_type = db.Column(db.Integer, CheckConstraint('book_type IN (1, 2, 3)'))
    book_status = db.Column(db.String(20), CheckConstraint("book_status IN ('Available', 'On_loan', 'Unavailable')"), default='Available')
    photo_url = db.Column(db.String(255)) 
    loans = db.relationship('Loans', back_populates='books')  # Relationship with Loans table

#Defining the Customers Table
class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(40))
    loans = db.relationship('Loans', back_populates='customers')  # Relationship with Loans table

#Defining the Loans Table
class Loans(db.Model):
    loan_id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    loan_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    condition_at_loan = db.Column(db.String(10), CheckConstraint("condition_at_loan IN ('Excellent', 'Good', 'Fair', 'Poor', 'Unusable')"), default='Excellent')
    fine_status = db.Column(db.Boolean, CheckConstraint('fine_status IN (0, 1)'), default=0)
    fine_amount = db.Column(db.Integer)
    loan_status = db.Column(db.String(20), CheckConstraint("loan_status IN ('Pending', 'Ongoing', 'Returned')"), default='Pending')
    customers = db.relationship('Customers', back_populates='loans')  # Relationship with Customers table
    books = db.relationship('Books', back_populates='loans')  # Relationship with Books table

#Defining Users Table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
   
@app.route('/')
def home():
        return "home"
                                            ###---Routes---###
                                            #-CRUD For Books Table-#

@app.route('/addbook', methods=['POST'])  # Create - Add a book to the library
def add_book():
    try:
        data = request.get_json()
        title = data.get("title")
        author = data.get("author")
        description = data.get("description")
        year_published = data.get("year_published")
        book_type = data.get("book_type")
        book_status = data.get("book_status")
        photo_url = data.get("photo_url")

        # Validate required fields
        if None in [title, author,description, year_published]:
            return jsonify({"error": "Missing required fields"}), 400
        # Validate data types if needed
        book = Books(title=title, author=author,description=description, year_published=year_published,
                     book_type=book_type, book_status=book_status, photo_url=photo_url)
        
        db.session.add(book)
        db.session.commit()

        return jsonify({"message": "Book successfully added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/books', methods=['GET'])  # Read - Display all Books in the Library
def get_books():
    try:
        books = []
        for book in Books.query.all():
            books.append({
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "description":book.description,
                "year_published": book.year_published,
                "book_type": book.book_type,
                "book_status": book.book_status,
                "photo_url": book.photo_url
            })
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Update
#Delete    

  #-CRUD For Customers Table-#
#Create
#Read
#Update
#Delete     

  #-CRUD For Loans Table-#  
#Create
#Read
#Update
#Delete 



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
  
   





