from app import app, db, User
from werkzeug.security import generate_password_hash
import os

with app.app_context():
    # 1. Clear everything and rebuild the tables
    db.drop_all()
    db.create_all()
    
    # 2. Create your user
    hashed_pw = generate_password_hash('password123', method='pbkdf2:sha256')
    new_user = User(username='ROwens03', password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    
    # 3. Diagnostic Info
    db_path = app.config['SQLALCHEMY_DATABASE_URI']
    print("\n" + "="*40)
    print(f"✅ DATABASE REBUILT AT: {db_path}")
    print(f"✅ USER CREATED: ROwens03")
    print(f"✅ PASSWORD SET TO: password123")
    print("="*40 + "\n")

print("Now, close this script and run: python app.py")