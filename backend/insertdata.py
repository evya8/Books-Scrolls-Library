# insertdata.py

from datetime import date
from app import app, db, Books, Customers, Loans, User, bcrypt

def insert_test_data():
    with app.app_context():
        # Insert test books
        book1 = Books(title="To Kill a Mockingbird", author="Harper Lee", year_published=1960, category="Fiction", book_type=1, book_status="Available", photo_url="static/images/bookcover.jpg")
        book2 = Books(title="1984", author="George Orwell", year_published=1949, category="Dystopian", book_type=2, book_status="On_loan", photo_url="static/images/bookcover.jpg")
        book3 = Books(title="Pride and Prejudice", author="Jane Austen", year_published=1813, category="Romance", book_type=3, book_status="Unavailable", photo_url="static/images/bookcover.jpg")
        book4 = Books(title="The Great Gatsby", author="F. Scott Fitzgerald", year_published=1925, category="Classic", book_type=1, book_status="Available", photo_url="static/images/bookcover.jpg")
        book5 = Books(title="One Hundred Years of Solitude", author="Gabriel García Márquez", year_published=1967, category="Magical Realism", book_type=2, book_status="On_loan", photo_url="static/images/bookcover.jpg")
        book6 = Books(title="The Hobbit", author="J.R.R. Tolkien", year_published=1937, category="Fantasy", book_type=3, book_status="Available", photo_url="static/images/static/images/bookcover.jpg")
        book7 = Books(title="The Catcher in the Rye", author="J.D. Salinger", year_published=1951, category="Coming of Age", book_type=1, book_status="On_loan", photo_url="static/images/static/images/bookcover.jpg")
        book8 = Books(title="War and Peace", author="Leo Tolstoy", year_published=1869, category="Historical Fiction", book_type=2, book_status="Unavailable", photo_url="static/images/static/images/bookcover.jpg")
        book9 = Books(title="The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", author="C.S. Lewis", year_published=1950, category="Children's Literature", book_type=3, book_status="Available", photo_url="static/images/bookcover.jpg")
        book10 = Books(title="The Da Vinci Code", author="Dan Brown", year_published=2003, category="Mystery", book_type=1, book_status="On_loan", photo_url="static/images/bookcover.jpg")
        book11 = Books(title="Crime and Punishment", author="Fyodor Dostoevsky", year_published=1866, category="Psychological Fiction", book_type=2, book_status="Unavailable", photo_url="static/images/bookcover.jpg")
        book12 = Books(title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling", year_published=1997, category="Young Adult", book_type=3, book_status="Available", photo_url="static/images/bookcover.jpg")
        book13 = Books(title="The Lord of the Rings", author="J.R.R. Tolkien", year_published=1954, category="High Fantasy", book_type=1, book_status="On_loan", photo_url="static/images/bookcover.jpg")
        book14 = Books(title="Anna Karenina", author="Leo Tolstoy", year_published=1877, category="Romantic Novel", book_type=2, book_status="Available", photo_url="static/images/bookcover.jpg")
        book15 = Books(title="The Shining", author="Stephen King", year_published=1977, category="Horror", book_type=3, book_status="On_loan", photo_url="static/images/bookcover.jpg")
        book16 = Books(title="Lonesome Dove", author="Larry McMurtry", year_published=1985, category="Western", book_type=2, book_status="Available", photo_url="static/images/bookcover.jpg")
        book17 = Books(title="The Picture of Dorian Gray", author="Oscar Wilde", year_published=1890, category="Gothic Fiction", book_type=2, book_status="Unavailable", photo_url="static/images/bookcover.jpg")
        book18 = Books(title="Brave New World", author="Aldous Huxley", year_published=1932, category="Science Fiction", book_type=3, book_status="Available", photo_url="static/images/bookcover.jpg")
        book19 = Books(title="The Jungle Book", author="Rudyard Kipling", year_published=1894, category="Children's Literature", book_type=1, book_status="On_loan", photo_url="static/images/bookcover.jpg")
        book20 = Books(title="The Hunchback of Notre-Dame", author="Victor Hugo", year_published=1831, category="Gothic Novel", book_type=2, book_status="Unavailable", photo_url="static/images/bookcover.jpg")

        db.session.add_all([book1, book2, book3, book4,book5,book6,book7,book8,book9,book10,book11,book12,book13,book14,book15,book16,book17,book18,book19,book20])
        db.session.commit()

        # Insert test customers
        customer1 = Customers(full_name="Alice Johnson", city="New York", age=28, phone_number=123456789, email="alice.johnson@example.com")
        customer2 = Customers(full_name="Bob Wilson", city="Los Angeles", age=35, phone_number=987654321, email="bob.wilson@example.com")
        customer3 = Customers(full_name="Eva Brown", city="Chicago", age=22, phone_number=555555555, email="eva.brown@example.com")
        customer4 = Customers(full_name="David Lee", city="Houston", age=40, phone_number=111111111, email="david.lee@example.com")
        customer5 = Customers(full_name="Samantha Taylor", city="Miami", age=33, phone_number=999999999, email="samantha.taylor@example.com")
        customer6 = Customers(full_name="Michael Turner", city="San Francisco", age=27, phone_number=444444444, email="michael.turner@example.com")
        customer7 = Customers(full_name="Olivia Davis", city="Seattle", age=29, phone_number=666666666, email="olivia.davis@example.com")
        customer8 = Customers(full_name="Daniel Martinez", city="Dallas", age=32, phone_number=777777777, email="daniel.martinez@example.com")
        customer9 = Customers(full_name="Sophia White", city="Atlanta", age=25, phone_number=888888888, email="sophia.white@example.com")
        customer10 = Customers(full_name="James Johnson", city="Phoenix", age=38, phone_number=222222222, email="james.johnson@example.com")

        db.session.add_all([customer1, customer2, customer3,customer4,customer5,customer6,customer7,customer8,customer9,customer10])
        db.session.commit()

        # Insert test loans
        loan1 = Loans(cust_id=1, book_id=1, loan_date=date(2022, 1, 1), return_date=date(2022, 1, 15), condition_at_loan="Good", fine_status=False, fine_amount=0, loan_status="Returned")
        loan2 = Loans(cust_id=2, book_id=2, loan_date=date(2022, 2, 1), return_date=date(2022, 2, 10), condition_at_loan="Excellent", fine_status=True, fine_amount=10, loan_status="Returned")
        loan3 = Loans(cust_id=3, book_id=3, loan_date=date(2022, 3, 1), return_date=date(2022, 3, 18), condition_at_loan="Fair", fine_status=False, fine_amount=0, loan_status="Returned")
        loan4 = Loans(cust_id=4, book_id=4, loan_date=date(2022, 4, 1), return_date=date(2022, 4, 20), condition_at_loan="Good", fine_status=True, fine_amount=5, loan_status="Returned")
        loan5 = Loans(cust_id=5, book_id=5, loan_date=date(2022, 5, 1), return_date=date(2022, 5, 12), condition_at_loan="Excellent", fine_status=False, fine_amount=0, loan_status="Returned")
        loan6 = Loans(cust_id=6, book_id=6, loan_date=date(2022, 6, 1), return_date=date(2022, 6, 15), condition_at_loan="Good", fine_status=False, fine_amount=0, loan_status="Returned")
        loan7 = Loans(cust_id=7, book_id=7, loan_date=date(2022, 7, 1), return_date=date(2022, 7, 10), condition_at_loan="Excellent", fine_status=True, fine_amount=15, loan_status="Returned")
        loan8 = Loans(cust_id=8, book_id=8, loan_date=date(2022, 8, 1), return_date=date(2022, 8, 22), condition_at_loan="Fair", fine_status=False, fine_amount=0, loan_status="Returned")
        loan9 = Loans(cust_id=9, book_id=9, loan_date=date(2022, 9, 1), return_date=date(2022, 9, 14), condition_at_loan="Good", fine_status=True, fine_amount=8, loan_status="Returned")
        loan10 = Loans(cust_id=10, book_id=10, loan_date=date(2022, 10, 1), return_date=date(2022, 10, 19), condition_at_loan="Excellent", fine_status=False, fine_amount=0, loan_status="Returned")
        loan11 = Loans(cust_id=1, book_id=11, loan_date=date(2022, 11, 1), return_date=date(2022, 11, 15), condition_at_loan="Good", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan12 = Loans(cust_id=2, book_id=12, loan_date=date(2022, 12, 1), return_date=date(2022, 12, 10), condition_at_loan="Excellent", fine_status=True, fine_amount=10, loan_status="Ongoing")
        loan13 = Loans(cust_id=3, book_id=13, loan_date=date(2023, 1, 1), return_date=date(2023, 1, 18), condition_at_loan="Fair", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan14 = Loans(cust_id=4, book_id=14, loan_date=date(2023, 2, 1), return_date=date(2023, 2, 20), condition_at_loan="Good", fine_status=True, fine_amount=5, loan_status="Ongoing")
        loan15 = Loans(cust_id=5, book_id=15, loan_date=date(2023, 3, 1), return_date=date(2023, 3, 12), condition_at_loan="Excellent", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan16 = Loans(cust_id=6, book_id=16, loan_date=date(2023, 4, 1), return_date=date(2023, 4, 15), condition_at_loan="Good", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan17 = Loans(cust_id=7, book_id=17, loan_date=date(2023, 5, 1), return_date=date(2023, 5, 10), condition_at_loan="Excellent", fine_status=True, fine_amount=15, loan_status="Ongoing")
        loan18 = Loans(cust_id=8, book_id=18, loan_date=date(2023, 6, 1), return_date=date(2023, 6, 22), condition_at_loan="Fair", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan19 = Loans(cust_id=9, book_id=19, loan_date=date(2023, 7, 1), return_date=date(2023, 7, 14), condition_at_loan="Good", fine_status=True, fine_amount=8, loan_status="Ongoing")
        loan20 = Loans(cust_id=10, book_id=20, loan_date=date(2023, 8, 1), return_date=date(2023, 8, 19), condition_at_loan="Excellent", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan21 = Loans(cust_id=1, book_id=1, loan_date=date(2023, 9, 1), return_date=date(2023, 9, 15), condition_at_loan="Good", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan22 = Loans(cust_id=2, book_id=2, loan_date=date(2023, 10, 1), return_date=date(2023, 10, 10), condition_at_loan="Excellent", fine_status=True, fine_amount=10, loan_status="Ongoing")
        loan23 = Loans(cust_id=3, book_id=3, loan_date=date(2023, 11, 1), return_date=date(2023, 11, 18), condition_at_loan="Fair", fine_status=False, fine_amount=0, loan_status="Ongoing")
        loan24 = Loans(cust_id=4, book_id=4, loan_date=date(2023, 12, 1), return_date=date(2023, 12, 20), condition_at_loan="Good", fine_status=True, fine_amount=5, loan_status="Ongoing")
        loan25 = Loans(cust_id=5, book_id=5, loan_date=date(2024, 1, 1), return_date=date(2024, 1, 12), condition_at_loan="Excellent", fine_status=False, fine_amount=0, loan_status="Ongoing")
       
        db.session.add_all([loan1, loan2, loan3, loan4, loan5, loan6, loan7, loan8, loan9, loan10, loan11, loan12, loan13, loan14, loan15, loan16, loan17, loan18, loan19, loan20, loan21, loan22, loan23, loan24, loan25])
        db.session.commit()

       # Insert test Users
        hashed_password_admina = bcrypt.generate_password_hash("youwontgetit").decode('utf-8')
        hashed_password_adminas = bcrypt.generate_password_hash("youcantgetit").decode('utf-8')
        hashed_password_billy = bcrypt.generate_password_hash("1a2b3c4d").decode('utf-8')

        user1 = User(username="Admina", password=hashed_password_admina, user_role="adminuet")
        user2 = User(username="Adminas", password=hashed_password_adminas, user_role="admensch")
        user3 = User(username="billy", password=hashed_password_billy, user_role="user")
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()

if __name__ == "__main__":
    insert_test_data()