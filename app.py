from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import barcode
from barcode.writer import ImageWriter


app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login' # Tells Flask where the login page is
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --------------------------
# Database Models
# --------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# --- FORM DEFINITION ---
class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Book')

class Book(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    author = db.Column(
        db.String(100),
        nullable=False
    )

    isbn = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )
class Sale(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Link to book
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('book.id'),
        nullable=False
    )

    # --- NEW: Snapshot Data for History ---
    book_title = db.Column(
        db.String(200),
        nullable=False
    )

    book_isbn = db.Column(
        db.String(20),
        nullable=False
    )

    # --- UPDATED: Allow Guests (nullable=True) ---
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True # <--- Set this to True for Guests
    )

    # Quantity sold
    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    # Store calculated values
    subtotal = db.Column(
        db.Float,
        nullable=False
    )

    tax = db.Column(
        db.Float,
        nullable=False
    )

    total = db.Column(
        db.Float,
        nullable=False
    )    
class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('book.id'),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(100),
        nullable=False
    )
    role = db.Column(
        db.String(20),
        nullable=False
    )

# --------------------------
# Create Default Users
# --------------------------

def create_default_users():

    users = [

        User(
            username="EBarreno01",
            password="EBarreno01",
            role="admin"
        ),

        User(
            username="JOspina02",
            password="JOspina02",
            role="admin"
        ),

        User(
            username="KPeekSM",
            password="KPeekSM",
            role="admin"
        ),

        User(
            username="ROwens03",
            password="ROwens03",
            role="admin"
        ),
        User(
            username="CPowersQA",
            password="CPowersQA",
            role="admin"
        ),
        User(
            username="FAlmasri01",
            password="FAlmasri01",
            role="user"
        )
    ]

    for user in users:

        existing = User.query.filter_by(
            username=user.username
        ).first()

        if not existing:
            db.session.add(user)

    db.session.commit()

# --------------------------
# Login Route
# --------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 1. Look up the user by username ONLY
        user = User.query.filter_by(username=username).first()
        
        # 2. Use check_password_hash to verify the password
        from werkzeug.security import check_password_hash
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")

            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            
            return redirect(next_page)
        else:
            flash("Invalid login credentials", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Officially ends the Flask-Login session
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

# --------------------------

# Dashboard
# --------------------------

@app.route('/dashboard')
@login_required # This replaces your 'if username not in session' check
def dashboard():
    # current_user is a special object that always knows who is logged in
    return render_template(
        'dashboard.html',
        username=current_user.username,
        role=current_user.role
    )


# --------------------------
# Book Management
# --------------------------
@app.route('/inventory')
@login_required 
def inventory():
    books = Book.query.all()
    return render_template('inventory.html', books=books, os=os)

@app.route('/books')
def books():
    # Fetch all books from the database
    all_books = Book.query.all()
    # Render the public storefront template
    return render_template('books.html', books=all_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = AddBookForm() # Create the form object
    
    if form.validate_on_submit():
        try:
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                isbn=form.isbn.data,
                price=form.price.data,
                quantity=form.quantity.data
            )
            db.session.add(new_book)
            db.session.commit()
            flash(f"Book '{form.title.data}' added successfully!", "success")
            return redirect(url_for('inventory'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {e}", "danger")

    # The CRITICAL part: Passing the form to the template
    return render_template('add_book.html', form=form)


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):

    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':

        try:

            book.title = request.form['title']
            book.author = request.form['author']
            book.isbn = request.form['isbn']
            book.price = float(request.form['price'])   
            book.quantity = int(request.form['quantity'])

            db.session.commit()

            flash(
                f"Book '{book.title}' updated successfully!",
                "success"
            )

            return redirect(url_for('books'))

        except Exception as e:

            flash(
                f"Error updating book: {e}",
                "danger"
            )

            return redirect(
                url_for('edit_book', book_id=book.id)
            )

    return render_template(
        'edit_book.html',
        book=book
    )


# --------------------------
# Delete Book
# --------------------------

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):

    book = Book.query.get_or_404(book_id)

    try:

        db.session.delete(book)
        db.session.commit()

        flash(
            f"Book '{book.title}' deleted successfully!",
            "success"
        )

    except Exception as e:

        flash(
            f"Error deleting book: {e}",
            "danger"
        )

    return redirect(url_for('books'))


# --------------------------
# Barcode Generator
# --------------------------

@app.route('/generate_barcode/<int:book_id>')
def generate_barcode(book_id):

    book = Book.query.get_or_404(book_id)

    isbn = book.isbn
    # Use'code128' to accept any numbers/tex
    code = barcode.get(
        'code128',
        isbn,
        writer=ImageWriter()
    )

    code.save(
        f"static/barcodes/{isbn}"
    )

    flash(
        "Barcode generated successfully!",
        "success"
    )

    return redirect(
        url_for('books')
    )

# TASK: Barcode Lookup Logic
@app.route('/api/check_book/<isbn>')
def api_check_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        return jsonify({
            'success': True,
            'id': book.id,
            'title': book.title,
            'price': book.price,
            'stock': book.quantity
        })
    return jsonify({'success': False, 'message': 'Book not found'})

# --------------------------
# Checkout
# --------------------------
@app.route('/checkout', methods=['GET', 'POST'])
# --- REMOVED @login_required ---
def checkout():
    books = Book.query.all()
    
    if request.method == 'POST':
        try:
            selected_book_id = int(request.form['book_id'])
            quantity = int(request.form['quantity'])
            
            book = Book.query.get_or_404(selected_book_id)
            
            if book.quantity < quantity:
                flash(f"Not enough stock! Only {book.quantity} copies left.", "danger")
                return redirect(url_for('checkout'))
            
            subtotal = book.price * quantity
            tax = subtotal * 0.06
            total = subtotal + tax
            
            new_sale = Sale(
                book_id=book.id,
                book_title=book.title,  
                book_isbn=book.isbn,    
                quantity=quantity,
                subtotal=round(subtotal, 2),
                tax=round(tax, 2),
                total=round(total, 2),
                # If your Sale model has a user_id, we use current_user.id if they are logged in, 
                # otherwise we leave it None or use a default 'Guest' ID.
                user_id=current_user.id if current_user.is_authenticated else None,
                date=datetime.now()
            )

            book.quantity -= quantity
            db.session.add(new_sale)
            db.session.commit()
            
            flash(f"Successfully purchased {quantity}x {book.title}!", "success")

            # --- LOGIC CHANGE FOR REDIRECT ---
            # If the user is an admin, take them to history. If guest, take them to the storefront.
            if current_user.is_authenticated and current_user.role == 'admin':
                return redirect(url_for('sales_history'))
            return redirect(url_for('books')) # Redirects guests back to your new storefront
            
        except Exception as e:
            db.session.rollback()
            flash(f"Transaction Error: {str(e)}", "danger")
            return redirect(url_for('checkout'))
            
    return render_template('checkout.html', books=books)

@app.route("/receipt/<int:sale_id>")
def receipt(sale_id):

    sale = Sale.query.get_or_404(
        sale_id
    )

    return render_template(
        "receipt.html",
        sale=sale
    )
# --------------------------
# Sales History
# --------------------------

@app.route('/sales_history')
def sales_history():

    sales = Sale.query.order_by(
        Sale.date.desc()
    ).all()

    return render_template(
        'sales_history.html',
        sales=sales
    )
# --------------------------
# Low Stock
# --------------------------

@app.route('/low_stock')
def low_stock():

    threshold = 5

    low_stock_books = Book.query.filter(
        Book.quantity <= threshold
    ).all()

    return render_template(
        'low_stock.html',
        books=low_stock_books,
        threshold=threshold
    )

# --------------------------
# Purchase Orders
# --------------------------

@app.route('/purchase_orders')
def purchase_orders():

    orders = PurchaseOrder.query.all()
    books = Book.query.all()

    return render_template(
        'purchase_orders.html',
        orders=orders,
        books=books
    )


@app.route('/add_purchase_order', methods=['POST'])
def add_purchase_order():

    try:

        book_id = int(request.form['book_id'])
        quantity = int(request.form['quantity'])

        order = PurchaseOrder(
            book_id=book_id,
            quantity=quantity
        )

        db.session.add(order)
        db.session.commit()

        flash(
            "Purchase order created.",
            "success"
        )

    except Exception as e:

        flash(
            f"Error creating order: {e}",
            "danger"
        )

    return redirect(
        url_for('purchase_orders')
    )


# --------------------------
# Suppliers
# --------------------------

@app.route('/seed_suppliers')
@login_required
def seed_suppliers():
    # Adding default Maryland/Regional suppliers for your demo
    demo_suppliers = [
        Supplier(name="Baltimore Book Distrib.", contact="orders@bmorebooks.com"),
        Supplier(name="Annapolis Paper Co.", contact="410-555-0199"),
        Supplier(name="DC Scholastic Hub", contact="dc-sales@scholastic.com")
    ]
    
    for s in demo_suppliers:
        existing = Supplier.query.filter_by(name=s.name).first()
        if not existing:
            db.session.add(s)
            
    db.session.commit()
    flash("Demo suppliers generated!", "info")
    return redirect(url_for('suppliers'))

@app.route('/suppliers')
def suppliers():

    all_suppliers = Supplier.query.all()

    return render_template(
        'suppliers.html',
        suppliers=all_suppliers
    )

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    try:
        name = request.form['name']
        contact = request.form.get('contact', '')

        # TASK: Validate Supplier (Check for duplicates)
        existing = Supplier.query.filter_by(name=name).first()
        if existing:
            flash(f"Supplier '{name}' already exists!", "warning")
            return redirect(url_for('suppliers'))

        supplier = Supplier(name=name, contact=contact)
        db.session.add(supplier)
        db.session.commit()
        flash("Supplier added successfully!", "success")

    except Exception as e:
        flash(f"Error adding supplier: {e}", "danger")

    return redirect(url_for('suppliers'))

# --- SUPPLIER MANAGEMENT ---

@app.route('/delete_supplier/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    try:
        db.session.delete(supplier)
        db.session.commit()
        flash('Supplier removed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: Could not remove supplier. {str(e)}', 'danger')
    
    return redirect(url_for('suppliers'))
# --------------------------
# Main

import os

with app.app_context():
    # TEMPORARY: Wipe and rebuild (Uncomment for the reset)
    #db.drop_all() 
    
    os.makedirs('static/barcodes', exist_ok=True) 
    db.create_all()
    create_default_users()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )