import os
import hashlib
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Length
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

# Security & Database Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the barcodes directory if it doesn't exist
os.makedirs(os.path.join('static', 'barcodes'), exist_ok=True)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# ==================== DATABASE MODELS ====================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- FORM DEFINITION ---
class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Book')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Link to book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    # Snapshot data for history
    book_title = db.Column(db.String(200), nullable=False)
    book_isbn = db.Column(db.String(20), nullable=False)

    # Allow guests
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

# ==================== DATABASE MODELS ====================
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== FORMS ====================
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# ==================== CORE ROUTES ====================
@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
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
@login_required
def dashboard():
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
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

# ==================== BOOK ACTIONS ====================

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBookForm()

    if form.validate_on_submit():
        try:
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                isbn=form.isbn.data,
                price=form.price.data,
                quantity=form.quantity.data,
                description=form.description.data
            )

            db.session.add(new_book)
            db.session.commit()

            flash(f"Book '{form.title.data}' added successfully!", "success")
            return redirect(url_for('inventory'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {e}", "danger")

    return render_template('add_book.html', form=form)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    # Fixes the 'edit_book' BuildError in the inventory
    book = Book.query.get_or_404(book_id)
    form = AddBookForm(obj=book) # Pre-fills the form with existing data
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.price = form.price.data
        book.quantity = form.quantity.data
        book.description = form.description.data
        db.session.commit()
        flash(f'Updated "{book.title}" successfully!', 'success')
        return redirect(url_for('inventory'))
    
    return render_template('edit_book.html', form=form, book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash(f'Deleted "{book.title}".', 'info')
    return redirect(url_for('inventory'))

@app.route('/generate_barcode/<int:book_id>')
@login_required
def generate_barcode(book_id):
    book = Book.query.get_or_404(book_id)
    isbn = book.isbn

    # Use code128 to accept any numbers/text
    barcode_dir = os.path.join(app.root_path, 'static', 'barcodes')
    if not os.path.exists(barcode_dir):
        os.makedirs(barcode_dir)

    code = barcode.get(
        'code128',
        isbn,
        writer=ImageWriter()
    )

    code.save(os.path.join(barcode_dir, isbn))

    flash("Barcode generated successfully!", "success")

    return render_template('barcode.html', book=book, barcode_url=f"barcodes/{isbn}.png")


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
                user_id=current_user.id if current_user.is_authenticated else None,
                date=datetime.now()
            )

            book.quantity -= quantity
            db.session.add(new_sale)
            db.session.commit()

            flash(f"Successfully purchased {quantity}x {book.title}!", "success")

            if current_user.is_authenticated and current_user.role == 'admin':
                return redirect(url_for('sales_history'))
            return redirect(url_for('books'))

        except Exception as e:
            db.session.rollback()
            flash(f"Transaction Error: {str(e)}", "danger")
            return redirect(url_for('checkout'))

    return render_template('checkout.html', books=books)

@app.route("/receipt/<int:sale_id>")
def receipt(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    return render_template("receipt.html", sale=sale)

# --------------------------
# Sales History
# --------------------------

@app.route('/sales_history')
@login_required
def sales_history():
    sales = Sale.query.order_by(Sale.date.desc()).all()
    return render_template('sales_history.html', sales=sales)

@app.route('/low_stock')
@login_required
def low_stock():
    threshold = 5
    books = Book.query.filter(Book.quantity <= threshold).all()
    return render_template('low_stock.html', books=books, threshold=threshold)

@app.route('/seed_suppliers')
@login_required
def seed_suppliers():
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
@login_required
def suppliers():
    all_suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=all_suppliers)

@app.route('/purchase_orders')
@login_required
def purchase_orders():
    orders = PurchaseOrder.query.all()
    books = Book.query.all()
    return render_template('purchase_orders.html', orders=orders, books=books)

@app.route('/add_purchase_order', methods=['POST'])
@login_required
def add_purchase_order():
    try:
        book_id = int(request.form['book_id'])
        quantity = int(request.form['quantity'])

        order = PurchaseOrder(book_id=book_id, quantity=quantity)
        db.session.add(order)
        db.session.commit()

        flash('Purchase order created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating purchase order: {e}', 'danger')

    return redirect(url_for('purchase_orders'))

@app.route('/add_supplier', methods=['POST'])
@login_required
def add_supplier():
    try:
        name = request.form['name']
        contact = request.form.get('contact', '')

        existing = Supplier.query.filter_by(name=name).first()
        if existing:
            flash(f"Supplier '{name}' already exists!", "warning")
            return redirect(url_for('suppliers'))

        supplier = Supplier(name=name, contact=contact)
        db.session.add(supplier)
        db.session.commit()
        flash("Supplier added successfully!", "success")

    except Exception as e:
        db.session.rollback()
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

# ==================== INITIALIZATION ====================
def init_db():
    with app.app_context():
        os.makedirs(os.path.join(app.root_path, 'static', 'barcodes'), exist_ok=True)
        db.create_all()

        users_to_create = [
            ('admin', 'admin123', 'admin'),
            ('ROwens03', 'ROwens03', 'admin'),
            ('J0spina02', 'J0spina02', 'admin'),
            ('EBarreno01', 'EBarreno01', 'admin'),
            ('KPeekSM', 'KPeekSM', 'admin'),
            ('CPowersQA', 'CPowersQA', 'admin'),
            ('FAlmasri01', 'FAlmasri01', 'user')
        ]

        for u, p, r in users_to_create:
            if not User.query.filter_by(username=u).first():
                new_user = User(username=u, role=r)
                new_user.set_password(p)
                db.session.add(new_user)

        db.session.commit()


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)