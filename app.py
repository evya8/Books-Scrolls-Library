
import os
from flask import Flask, render_template  , request , jsonify 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'your_secret_key'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasebooksandscrolls.db'  # Use SQLite database named 'databasebooksandscrolls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)  # Set the expiration time for token
app.config["JWT_ALGORITHM"] = "HS256"  # Set the algorithm
jwt = JWTManager(app)    # Initialize JWT 
# Upload folder and default image configuration
app.config["UPLOAD_FOLDER"] = "static/images/uploads"
app.config["DEFAULT_IMG"] = "static/images/bookcover.jpeg"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#Defining the Books Table
class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30))
    category = db.Column(db.String(15))
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
    loan_status = db.Column(db.String(20), CheckConstraint("loan_status IN ('Pending', 'Ongoing','Late', 'Returned')"), default='Pending')
    customers = db.relationship('Customers', back_populates='loans')  # Relationship with Customers table
    books = db.relationship('Books', back_populates='loans')  # Relationship with Books table

#Defining Users Table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    user_role = db.Column(db.String(50), default='user')  

@app.route('/')
def home():
    return "Please Run index.html with live server"
        
                                                    ###---Routes---###
                                                    #----------------CRUD For Books Table------------#

@app.route('/add_book', methods=['POST'])              ## Create - Add a book to the library
def add_book():
    try:
        data = request.get_json()
        title = data.get("title")
        author = data.get("author")
        category = data.get("category")
        description = data.get("description")
        year_published = data.get("year_published")
        book_type = data.get("book_type")
        book_status = data.get("book_status")
        photo_url = data.get("photo_url")

        # Validate required fields
        if None in [title, author,category,description, year_published]:
            return jsonify({"error": "Missing required fields"}), 400
        # Validate data types if needed
        book = Books(title=title, author=author,description=description, year_published=year_published,
                     book_type=book_type, book_status=book_status, photo_url=photo_url)
        
        db.session.add(book)
        db.session.commit()

        return jsonify({"message": "Book successfully added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
                                               ## Read - Display all Books in the Library
@app.route('/books', methods=['GET', 'OPTIONS'])
def get_books():
    try:
        title = request.args.get('title')

        if title:
            # If a title is provided, filter by title
            books_data = Books.query.filter(Books.title.ilike(f"%{title}%")).all()
        else:
            # If no title is provided, get all books
            books_data = Books.query.all()

        # Convert book types based on your logic
        for book in books_data:
            if book.book_type == 1:
                book.book_type = "10 Days"
            elif book.book_type == 2:
                book.book_type = "5 Days"
            elif book.book_type == 3:
                book.book_type = "2 Days"
            else:
                return jsonify({"error": "Invalid book type"}), 400

        # Consolidate the data into a list of dictionaries
        books = [
            {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "category": book.category,
                "description": book.description,
                "year_published": book.year_published,
                "book_type": book.book_type,  # Updated book type
                "book_status": book.book_status,
                "photo_url": book.photo_url
            }
            for book in books_data
        ]
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
                          
@app.route('/upd_book/<int:book_id>', methods=['OPTIONS', 'PUT'])         ## Update - Update and change Book details
def upd_book(book_id):
 
    book_to_update = Books.query.get(book_id)
    
    if not book_to_update:                              # Checking the book exist
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'PUT':                        # Update book details from the JSON data
        try:
            data = request.get_json()
            book_to_update.title = data.get('title', book_to_update.title)
            book_to_update.author = data.get('author', book_to_update.author)
            book_to_update.category = data.get('category', book_to_update.category)
            book_to_update.description = data.get('description', book_to_update.description)
            book_to_update.year_published = data.get('year_published', book_to_update.year_published)
            book_to_update.book_type = data.get('book_type', book_to_update.book_type)
            book_to_update.book_status = data.get('book_status', book_to_update.book_status)
            book_to_update.photo_url = data.get('photo_url', book_to_update.photo_url)
      
            db.session.commit()           # Commit the changes to the database
            return jsonify({'message': f'The Book "{book_to_update.title}" was updated successfully'}), 204
        except Exception as e:
           
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
        # Retrieve the 'full_name' parameter from request.args
        full_name = request.args.get('full_name')

        # Check if a search term is provided
        if full_name:
            # Perform a case-insensitive search using LIKE
            customers_data = Customers.query.filter(Customers.full_name.ilike(f"%{full_name}%")).all()
        else:
            # If no search term, return all customers
            customers_data = Customers.query.all()

        # Convert the customers data to a list of dictionaries
        customers_info = [
            {
                "customer_id": customer.customer_id,
                "full_name": customer.full_name,
                "city": customer.city,
                "age": customer.age,
                "phone_number": customer.phone_number,
                "email": customer.email
            }
            for customer in customers_data
        ]

        return jsonify(customers_info)

    except Exception as e:
        print(e)
        return jsonify({"error": "Unable to fetch customer data"}), 500


 
@app.route('/upd_customer/<int:customer_id>', methods=['PUT'])         ## Update - Update and change Customer details
def upd_customer(customer_id):
    customer_to_update = Customers.query.get(customer_id)
    if not customer_to_update:                              # Checking the Customer exist
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
            customer_to_del=Customers.query.get(int(customer_id))       # Checking the Customer exist
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
        cust_id = data.get("cust_id")
        book_id = data.get("book_id")
        loan_date = datetime.now().date()
        return_date = data.get("return_date")
        condition_at_loan = data.get("condition_at_loan")
        loan_status = data.get("loan_status")

        # Get the book type to calculate return_date
        book_type = Books.query.filter_by(book_id=book_id).first().book_type
        if book_type == 1:
            return_date = loan_date + timedelta(days=10)
        elif book_type == 2:
            return_date = loan_date + timedelta(days=5)
        elif book_type == 3:
            return_date = loan_date + timedelta(days=2)
        else:
            return jsonify({"error": "Invalid book type"}), 400

        # Validate required fields
        if None in [ book_id,book_type,cust_id,condition_at_loan]:
            return jsonify({"error": "Missing required fields"}), 400
        # Validate data types if needed
        loan = Loans(cust_id=cust_id, book_id=book_id,loan_date=loan_date , return_date=return_date,
                     condition_at_loan=condition_at_loan, loan_status=loan_status)
        
        db.session.add(loan)
        db.session.commit()

        return jsonify({"message": "Loan successfully added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500        
    
@app.route('/loans', methods=['GET'])                    ## Read - Display all Loans in the Library
def get_loans():
    try:
        loans = []
        for loan in Loans.query.all():
            # Calculate the fine if the book is not returned yet
            if loan.loan_status != 'Returned':
                current_date = datetime.now().date()
                if current_date > loan.return_date:
                    days_late = (current_date - loan.return_date).days
                    fine_rate_per_day = 0.5 
                    fine_amount = days_late * fine_rate_per_day
                    loan.fine_status = True
                    loan.fine_amount = fine_amount
                    loan.loan_status = 'Late'
                else:
                    loan.fine_status = False
                    loan.fine_amount = 0
            loans.append({
                "loan_id": loan.loan_id,
                "cust_id": loan.cust_id,
                "book_id": loan.book_id,
                "loan_date": loan.loan_date,
                "return_date":loan.return_date,
                "condition_at_loan": loan.condition_at_loan,
                "fine_status": loan.fine_status,
                "fine_amount": loan.fine_amount,
                "loan_status": loan.loan_status
            })
        return jsonify(loans)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
@app.route('/upd_loan/<int:loan_id>', methods=['PUT'])         ## Update - Update and change Loan details
def upd_loan(loan_id):
    loan_to_update = Loans.query.get(loan_id)
    if not loan_to_update:                              # Checking the Loan exist
        return jsonify({"error": "Loan not found"}), 404

    if request.method == 'PUT':                        # Update Loan details from the JSON data
        try:
            data = request.get_json()
            loan_to_update.cust_id = data.get('cust_id', loan_to_update.cust_id)
            loan_to_update.book_id = data.get('book_id', loan_to_update.book_id)
            loan_to_update.loan_date = data.get('loan_date', loan_to_update.loan_date)
            loan_to_update.return_date = data.get('return_date', loan_to_update.return_date)
            loan_to_update.condition_at_loan = data.get('condition_at_loan', loan_to_update.condition_at_loan)
            loan_to_update.fine_status = data.get('fine_status', loan_to_update.fine_status)
            loan_to_update.fine_amount = data.get('fine_amount', loan_to_update.fine_amount)
            loan_to_update.loan_status = data.get('loan_status', loan_to_update.loan_status)
            # Update return_date only if loan_status is 'Returned'
            if data.get('loan_status') == 'Returned':
                loan_to_update.return_date = datetime.now().date()
            
            db.session.commit()           # Commit the changes to the database
            return jsonify({'message': f'Loan with ID "{loan_to_update.loan_id}" was updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating Loan: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid request method'}), 405

@app.route("/del_loan/<int:loan_id>", methods=['DELETE'])             ## Delete - Remove a Loan from Library records 
def loan(loan_id):
        try:
            loan_to_del=Loans.query.get(int(loan_id))       # Checking the Loan exist
            if loan_to_del:
                db.session.delete(loan_to_del)
                db.session.commit()                  # Commit the changes to the database
                return jsonify({"message": f'The Loan with ID number "{loan_to_del.loan_id}" was deleted successfully'}), 200
            return jsonify({"error": "Loan not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error deleting book: {str(e)}"}), 500     
 
                                                        #---------------- Login/Register------------#
            
                                                            ## User register
@app.route('/user/register', methods=['POST'])
def register():

    data=request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Check if the username is already taken
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username is already taken'}), 400

    # # Hash and salt the password using Bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # # Create a new user and add to the database
    new_user = User(username=username, password=hashed_password,user_role="user")
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/user/login', methods=['POST'])                 ## User login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
    
        return jsonify(), 200




                                                    #-----------Images Routes (Upload and Display)---------------#
@app.route('/upload',methods=['POST'])     ## Upload the image
def upload():
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return {'message': 'success', 'filename': file.filename}, 201
        return {'message': 'File upload failed'}, 500

@app.route('/images', methods=['GET'])      ## Displays the images
def get_images():
    image_list = []
    upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    for filename in os.listdir(upload_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust for other image formats if needed
            image_list.append(f"http://127.0.0.1:5000/uploads/{filename}")  # Replace with your server URL and path
    return jsonify({'images': image_list})


                                                 ## Customer Library card



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)