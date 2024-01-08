# Books Library Management System

This project was created by Evyatar Hermesh to implement a simple system to manage a library of books using Flask, SQLite,Axios and RESTful API. The system includes three main entities: Books, Customers, and Loans, with relationships between them to track book loans to customers.

First I will lay out the project for you to know it, then I will walk you through installing and running it.

## Database Structure

1. **Books Table:**
   - **Id (PK):** Primary key for each book.
   - **Title:** Title of the book.
   - **Author:** Author of the book.
   - **Year Published:** Year the book was published.
   - **Type (1/2/3):** Book type, determining the maximum loan time.
   - **Book Status:** Is this book loaned or avialable to loan.

2. **Customers Table:**
   - **Id (PK):** Primary key for each customer.
   - **Name:** Name of the customer.
   - **City:** City of residence of the customer.
   - **Age:** Age of the customer.
   - **Phone Number:** Phone Number of the customer.
   - **Email:** Email Address of the customer.

3. **Loans Table:**
   - **CustID:** Foreign key referencing a customer's Id.
   - **BookID:** Foreign key referencing a book's Id.
   - **Loandate:** Date when the book was borrowed.
   - **Returndate:** Date when the book is expected to be returned.
   - **Condition At Loan:** The physical condition of the book when loaned.
   - **Fine Status:** Tracks for overdue returns.
   - **Fine Amount:** Calculate the amount of fine when applicable.
   - **Status:** The status of the loan : default - Pending , Ongoing and Returned
   

## Maximum Loan Time Based on Book Type

The book type determines the maximum loan time for a book:
- **Type 1:** Up to 10 days
- **Type 2:** Up to 5 days
- **Type 3:** Up to 2 days

## Data Access Layer (DAL)

The Data Access Layer is implemented with classes for each entity using SQLAlchemy (Books, Customers, Loans). Each class has a separate module, and unit tests are provided to ensure proper functionality.

### DAL Modules:
- **`books`:** Defines the `Books` class for book-related operations.
- **`customers`:** Defines the `Customers` class for customer-related operations.
- **`loans`:** Defines the `Loans` class for loan-related operations.

### Unit Tests:
- **`test_books.py`:** Unit tests for the `Books` class.
- **`test_customers.py`:** Unit tests for the `Customers` class.
- **`test_loans.py`:** Unit tests for the `Loans` class.

## Client Application

A client application is built to interact with the DAL. The application facilitates Resgister and Login of users with restricted access to some features. Each user will have upon login his page where he can see what books he loaned and if there are active loans.
The client application provides a simple menu-driven interface with the following operations:

1. Add a new customer
2. Add a new book
3. Loan a book
4. Return a book
5. Display all books
6. Display all customers
7. Display all loans
8. Display late loans
9. Find book by name
10. Find customer by name
11. Remove customer

## Getting Started

1. Start new project
2. Open Virtual env
3. Install Requirements.txt
4. Run the Flask app: `python app.py` MAC : `python3 app.py`
5. Open browser at local to view project

Feel free to enhance the project for production use by adding features like authentication, error handling, and security measures.