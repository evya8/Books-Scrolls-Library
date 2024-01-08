# insertdata.py

from datetime import date
from app import app, db, Books, Customers, Loans

def insert_test_data():
    with app.app_context():
        # Insert test books
        book1 = Books(title="Book 1", author="Author 1", year_published=2020, book_type=1, book_status="Available", photo_url="book1.jpg")
        book2 = Books(title="Book 2", author="Author 2", year_published=2018, book_type=2, book_status="On_loan", photo_url="book2.jpg")
        book3 = Books(title="Book 3", author="Author 3", year_published=2015, book_type=3, book_status="Unavailable", photo_url="book3.jpg")
        
        db.session.add_all([book1, book2, book3])
        db.session.commit()

        # Insert test customers
        customer1 = Customers(full_name="Customer 1", city="City 1", age=25, phone_number=123456789, email="customer1@example.com")
        customer2 = Customers(full_name="Customer 2", city="City 2", age=30, phone_number=987654321, email="customer2@example.com")
        
        db.session.add_all([customer1, customer2])
        db.session.commit()

        # Insert test loans
        loan1 = Loans(cust_id=1, book_id=1, loan_date=date(2022, 1, 1), return_date=date(2022, 1, 15), condition_at_loan="Good", fine_status=False, fine_amount=0, loan_status="Returned")
        loan2 = Loans(cust_id=2, book_id=2, loan_date=date(2022, 2, 1), return_date=date(2022, 2, 10), condition_at_loan="Excellent", fine_status=True, fine_amount=10, loan_status="Ongoing")
        
        db.session.add_all([loan1, loan2])
        db.session.commit()

if __name__ == "__main__":
    insert_test_data()
