from app import app, db, User, Book, Supplier  # Added Book and Supplier
import os

with app.app_context():

    db.drop_all()
    db.create_all()

    # 2. List of all Admin Accounts
    admin_usernames = [
        'EBarreno01', 'JOspina02', 'ROwens03', 
        'KPeekSM', 'CPowers04', 'FAlmarasiFadi01', 'SShad02'
    ]

    print("\n" + "="*40)
    for username in admin_usernames:
        new_user = User(
            username=username, 
            role='admin'  
        )
        new_user.set_password(username)
        db.session.add(new_user)
        print(f"✅ ADMIN CREATED: {username} (Password: {username})")

    db.session.commit()

# 3. Seed the Inventory with Demo Books
    print("Seeding Book Inventory...")
    demo_books = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565', 'price': 15.00, 'qty': 10},
        {'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'price': 12.50, 'qty': 15},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'isbn': '9780547928227', 'price': 20.00, 'qty': 8},
        {'title': 'Atomic Habits', 'author': 'James Clear', 'isbn': '9780735211292', 'price': 18.00, 'qty': 20}
    ]

    for data in demo_books:
        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            price=data['price'],
            quantity=data['qty']
        )
        db.session.add(new_book)
        print(f"📖 Added Book: {data['title']}")

    # 4. Seed Demo Suppliers
    print("Seeding Suppliers...")
    suppliers = [
        {'name': 'Baltimore Book Distrib.', 'contact': 'orders@bmorebooks.com'},
        {'name': 'Annapolis Paper Co.', 'contact': '410-555-0199'},
        {'name': 'DC Scholastic Hub', 'contact': 'dc-sales@scholastic.com'}
    ]

    for s in suppliers:
        db.session.add(Supplier(name=s['name'], contact=s['contact']))
    
    db.session.commit()
    print("\n✅ SEEDING COMPLETE: 4 Books and 3 Suppliers added.")    

    # 3. Diagnostic Info
    db_path = app.config['SQLALCHEMY_DATABASE_URI']
    print("="*40)
    print(f"✅ DATABASE REBUILT AT: {db_path}")
    print("✅ AUTH RULE: Password matches Username for all admins.")
    print("="*40 + "\n")

print("Now, close this script and run: python app.py")