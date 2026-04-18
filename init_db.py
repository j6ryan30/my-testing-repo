from app import app, db, User, Book, Supplier

def init_db():
    with app.app_context():
        db.drop_all()     
        db.create_all()

    admin_usernames = [
        'EBarreno01', 'JOspina02', 'ROwens03',
        'KPeekSM', 'CPowers04', 'FAlmarasiFadi01', 'SShad02'
    ]

    print("\n" + "=" * 40)
    for username in admin_usernames:
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username=username, role='admin')
            new_user.set_password(username)
            db.session.add(new_user)
            print(f"✅ ADMIN CREATED: {username}")

    demo_books = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '9780743273565', 'price': 15.00, 'qty': 10, 'description': 'Classic American novel set in the Jazz Age.'},
        {'title': '1984', 'author': 'George Orwell', 'isbn': '9780451524935', 'price': 12.50, 'qty': 15, 'description': 'Dystopian novel about surveillance and totalitarianism.'},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'isbn': '9780547928227', 'price': 20.00, 'qty': 8, 'description': 'Fantasy adventure featuring Bilbo Baggins.'},
        {'title': 'Attack on Titan', 'author': 'Hajime Isayama', 'isbn': '9780316201234', 'price': 15.99, 'qty': 10, 'description': 'Post-apocalyptic manga series.'},
        {'title': 'Atomic Habits', 'author': 'James Clear', 'isbn': '9780735211292', 'price': 18.00, 'qty': 20, 'description': 'Practical guide to building good habits.'},
        {'title': 'Harry Potter', 'author': 'J.K. Rowling', 'isbn': '123456789874', 'price': 20.99, 'qty': 25, 'description': 'Popular fantasy novel about a young wizard.'}
    ]

    print("Seeding Book Inventory...")
    for data in demo_books:
        existing_book = Book.query.filter_by(isbn=data['isbn']).first()
        if not existing_book:
            new_book = Book(
                title=data['title'],
                author=data['author'],
                isbn=data['isbn'],
                price=data['price'],
                quantity=data['qty'],
                description=data['description']
            )
            db.session.add(new_book)
            print(f"📖 Added Book: {data['title']}")

    print("Seeding Suppliers...")
    suppliers = [
        {'name': 'Baltimore Book Distrib.', 'contact': 'orders@bmorebooks.com'},
        {'name': 'Annapolis Paper Co.', 'contact': '410-555-0199'},
        {'name': 'DC Scholastic Hub', 'contact': 'dc-sales@scholastic.com'}
    ]

    for s in suppliers:
        existing_supplier = Supplier.query.filter_by(name=s['name']).first()
        if not existing_supplier:
            db.session.add(Supplier(name=s['name'], contact=s['contact']))
            print(f"🏢 Added Supplier: {s['name']}")

    db.session.commit()
    print("\n✅ SAFE INIT COMPLETE\n")