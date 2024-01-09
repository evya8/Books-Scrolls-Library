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
                                                    #----------------CRUD For Books Table------------#

@app.route('/add_book', methods=['POST'])              ## Create - Add a book to the library
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
    
@app.route('/books', methods=['GET'])                    ## Read - Display all Books in the Library
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
      
@app.route('/upd_book/<int:book_id>', methods=['PUT'])         ## Update - Update and change Book details
def upd_book(book_id):
    book_to_update = Books.query.get(book_id)
    if not book_to_update:                              # Checking the book exist
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'PUT':                        # Update book details from the JSON data
        try:
            data = request.get_json()
            book_to_update.title = data.get('title', book_to_update.title)
            book_to_update.author = data.get('author', book_to_update.author)
            book_to_update.description = data.get('description', book_to_update.description)
            book_to_update.year_published = data.get('year_published', book_to_update.year_published)
            book_to_update.book_type = data.get('book_type', book_to_update.book_type)
            book_to_update.book_status = data.get('book_status', book_to_update.book_status)
            book_to_update.photo_url = data.get('photo_url', book_to_update.photo_url)

            db.session.commit()           # Commit the changes to the database
            return jsonify({'message': f'The Book "{book_to_update.title}" was updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating book: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid request method'}), 405


@app.route("/del_book/<int:book_id>", methods=['DELETE'])             ## Delete - Remove a Book from Library records 
def book(book_id):
        try:
            book_to_del=Books.query.get(int(book_id))       # Checking the book exist
            if book_to_del:
                db.session.delete(book_to_del)
                db.session.commit()                  # Commit the changes to the database
                return jsonify({"message": f'The Book "{book_to_del.title}" was deleted successfully'}), 200
            return jsonify({"error": "Book not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error deleting book: {str(e)}"}), 500

                                                    #-----------CRUD For Customers Table----------------#
        
@app.route('/add_customer', methods=['POST'])              ## Create - Add New Customer
def add_customer():
    try:
        data = request.get_json()
        full_name = data.get("full_name")
        city = data.get("city")
        age = data.get("age")
        phone_number = data.get("phone_number")
        email = data.get("email")

        # Validate required fields
        if None in [full_name, phone_number,email]:
            return jsonify({"error": "Missing required fields"}), 400
        # Validate data types if needed
        customer = Customers(full_name=full_name, city=city,age=age, phone_number=phone_number,
                     email=email)
        
        db.session.add(customer)
        db.session.commit()

        return jsonify({"message": "Customer successfully added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500        
    
@app.route('/customers', methods=['GET'])                    ## Read - Display all Customers of the Library
def get_customers():
    try:
        customers = []
        for customer in Customers.query.all():
            customers.append({
                "customer_id": customer.customer_id,
                "full_name": customer.full_name,
                "city": customer.city,
                "age":customer.age,
                "phone_number": customer.phone_number,
                "email": customer.email
            })
        return jsonify(customers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/upd_customer/<int:customer_id>', methods=['PUT'])         ## Update - Update and change Customer details
def upd_customer(customer_id):
    customer_to_update = Customers.query.get(customer_id)
    if not customer_to_update:                              # Checking the customer exist
        return jsonify({"error": "Customer not found"}), 404

    if request.method == 'PUT':                        # Update customer details from the JSON data
        try:
            data = request.get_json()
            customer_to_update.full_name = data.get('full_name', customer_to_update.full_name)
            customer_to_update.city = data.get('city', customer_to_update.city)
            customer_to_update.age = data.get('age', customer_to_update.age)
            customer_to_update.phone_number = data.get('phone_number', customer_to_update.phone_number)
            customer_to_update.email = data.get('email', customer_to_update.email)
            
            db.session.commit()           # Commit the changes to the database
            return jsonify({'message': f'The Customer "{customer_to_update.full_name}" details were updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating customer: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid request method'}), 405

@app.route("/del_customer/<int:customer_id>", methods=['DELETE'])             ## Delete - Remove a Customer from Library records 
def customer(customer_id):
        try:
            customer_to_del=Customers.query.get(int(customer_id))       # Checking the customer exist
            if customer_to_del:
                db.session.delete(customer_to_del)
                db.session.commit()                  # Commit the changes to the database
                return jsonify({"message": f'The Customer "{customer_to_del.full_name}" was deleted successfully'}), 200
            return jsonify({"error": "Customer not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error deleting book: {str(e)}"}), 500     

                                                    #--------------CRUD For Loans Table----------------#  

@app.route('/add_loan', methods=['POST'])              ## Create - Add New Loan
def add_loan():
    try:
        data = request.get_json()
        full_name = data.get("full_name")
        city = data.get("city")
        age = data.get("age")
        phone_number = data.get("phone_number")
        email = data.get("email")

        # Validate required fields
        if None in [full_name, phone_number,email]:
            return jsonify({"error": "Missing required fields"}), 400
        # Validate data types if needed
        customer = Customers(full_name=full_name, city=city,age=age, phone_number=phone_number,
                     email=email)
        
        db.session.add(customer)
        db.session.commit()

        return jsonify({"message": "Customer successfully added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500        
    
@app.route('/customers', methods=['GET'])                    ## Read - Display all Customers of the Library
def get_customers():
    try:
        customers = []
        for customer in Customers.query.all():
            customers.append({
                "customer_id": customer.customer_id,
                "full_name": customer.full_name,
                "city": customer.city,
                "age":customer.age,
                "phone_number": customer.phone_number,
                "email": customer.email
            })
        return jsonify(customers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/upd_customer/<int:customer_id>', methods=['PUT'])         ## Update - Update and change Customer details
def upd_customer(customer_id):
    customer_to_update = Customers.query.get(customer_id)
    if not customer_to_update:                              # Checking the customer exist
        return jsonify({"error": "Customer not found"}), 404

    if request.method == 'PUT':                        # Update customer details from the JSON data
        try:
            data = request.get_json()
            customer_to_update.full_name = data.get('full_name', customer_to_update.full_name)
            customer_to_update.city = data.get('city', customer_to_update.city)
            customer_to_update.age = data.get('age', customer_to_update.age)
            customer_to_update.phone_number = data.get('phone_number', customer_to_update.phone_number)
            customer_to_update.email = data.get('email', customer_to_update.email)
            
            db.session.commit()           # Commit the changes to the database
            return jsonify({'message': f'The Customer "{customer_to_update.full_name}" details were updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating customer: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid request method'}), 405

@app.route("/del_customer/<int:customer_id>", methods=['DELETE'])             ## Delete - Remove a Customer from Library records 
def customer(customer_id):
        try:
            customer_to_del=Customers.query.get(int(customer_id))       # Checking the customer exist
            if customer_to_del:
                db.session.delete(customer_to_del)
                db.session.commit()                  # Commit the changes to the database
                return jsonify({"message": f'The Customer "{customer_to_del.full_name}" was deleted successfully'}), 200
            return jsonify({"error": "Customer not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error deleting book: {str(e)}"}), 500     




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
  
   





