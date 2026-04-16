# Noble Bookstore Management System

## Overview

The Noble Bookstore Management System is a Flask-based web application designed to manage bookstore inventory, user authentication, and barcode generation for books.

This project was developed as part of a team-based software development assignment using Python, Flask, SQLAlchemy, and Git version control.

The system allows administrators and users to log in, manage books, and generate barcodes for inventory tracking.

---

## Features

* User login authentication
* Role-based access (Admin/User)
* Book inventory management
* Add, edit, and delete books
* Barcode generation for books
* SQLite database backend
* Web-based interface using Flask
* Team collaboration using GitHub

---

## Technologies Used

* Python 3
* Flask
* Flask-SQLAlchemy
* Flask-WTF
* SQLite Database
* HTML / CSS (Jinja Templates)
* Python Barcode Library
* Git & GitHub

---

## Project Structure

noble-bookstore-team/
│
├── app.py                # Main Flask application
├── seed_users.py         # Script to create default users
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── inventory.html
│   ├── barcode.html
│   └── ...
│
├── static/               # Static files (CSS, images, barcodes)
│
├── instance/             # SQLite database storage
│   └── bookstore.db

---

## Installation Instructions

Follow these steps to run the project locally.

### Step 1 — Clone Repository

git clone https://github.com/YOUR-REPO-LINK.git

cd noble-bookstore-team

---

### Step 2 — Create Virtual Environment

Windows:

python -m venv venv

venv\Scripts\activate

---

### Step 3 — Install Dependencies

pip install -r requirements.txt

---

### Step 4 — Create Default Users

Run the seed script:

python seed_users.py

This creates the default login accounts.

---

### Step 5 — Run the Application

python app.py

Open browser:

http://127.0.0.1:5000

---

## Default Login Credentials

Admin Accounts:

Username: admin
Password: admin123

Username: EBarreno01
Password: EBarreno01

Username: ROwens03
Password: ROwens03

Username: JOspina02
Password: JOspina02

Username: KPeekSM
Password: KPeekSM

Username: CPowersQA
Password: CPowersQA

User Account:

Username: FAlmasri01
Password: FAlmasri01

---

## Database

The application uses SQLite as the database.

Database file location:

instance/bookstore.db

Users and tables are created automatically when:

python seed_users.py

is executed.

---

## Barcode Generation

The system generates barcode images for books using:

python-barcode
Pillow

Barcodes are saved inside the static directory and can be printed directly from the application.

---

## Team Members

(Add your team members here)

* Enrique Barreno
* (Add teammate names)
* (Add teammate names)

---

## How to Update the Project

Pull latest changes:

git pull origin main

Add changes:

git add .

Commit:

git commit -m "Update message"

Push:

git push origin main

---

## Troubleshooting

### Login Not Working

Run:

python seed_users.py

Then restart:

python app.py

---

### Missing Dependencies

Run:

pip install -r requirements.txt

---

### Database Issues

Delete:

instance/bookstore.db

Then run:

python seed_users.py

---

## Future Improvements

* Search functionality
* Export inventory reports
* Improved UI design
* Barcode scanning support
* User management dashboard

---

## License

This project is intended for educational purposes only.

---

## Acknowledgments

Developed as part of a Computer Science academic project using Flask and Python.
