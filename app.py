from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from wtforms import StringField, FloatField, TextAreaField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, NumberRange, Length
from flask_wtf import FlaskForm
from functools import wraps
import hashlib
import os
=======
from datetime import datetime
import barcode
from barcode.writer import ImageWriter
>>>>>>> 294f536 (Updated database models and barcode features)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================
class User(db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Hash and set password."""
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """Check if password matches."""
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class Book(db.Model):
<<<<<<< HEAD
    """Book model for inventory."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        """Convert book to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'description': self.description
        }
=======
>>>>>>> 294f536 (Updated database models and barcode features)

    id = db.Column(
        db.Integer,
        primary_key=True
    )

<<<<<<< HEAD
# ==================== FORMS WITH VALIDATION ====================
class AddBookForm(FlaskForm):
    """Form to add a new book."""
    title = StringField('Book Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=2, max=200, message='Title must be between 2 and 200 characters')
    ])
    author = StringField('Author', validators=[
        DataRequired(message='Author is required'),
        Length(min=2, max=120, message='Author name must be between 2 and 120 characters')
    ])
    price = FloatField('Price', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='Description cannot exceed 1000 characters')
    ])
    submit = SubmitField('Add Book')
=======
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
>>>>>>> 294f536 (Updated database models and barcode features)


class EditBookForm(FlaskForm):
    """Form to edit an existing book."""
    title = StringField('Book Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=2, max=200, message='Title must be between 2 and 200 characters')
    ])
    author = StringField('Author', validators=[
        DataRequired(message='Author is required'),
        Length(min=2, max=120, message='Author name must be between 2 and 120 characters')
    ])
    price = FloatField('Price', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='Description cannot exceed 1000 characters')
    ])
    submit = SubmitField('Update Book')


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    submit = SubmitField('Login')


# ==================== AUTHENTICATION HELPER ====================
def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================
@app.route('/')
def home():
    """Display the homepage with all books."""
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Display details for a specific book."""
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/api/books')
def api_books():
    """API endpoint to get all books as JSON."""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

<<<<<<< HEAD

@app.route('/api/books/<int:book_id>')
def api_book_detail(book_id):
    """API endpoint to get a specific book as JSON."""
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.to_dict())
=======
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
>>>>>>> 294f536 (Updated database models and barcode features)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('inventory'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/inventory')
@login_required
def inventory():
    """Display inventory management screen (admin view)."""
    books = Book.query.all()
    return render_template('inventory.html', books=books)


@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
<<<<<<< HEAD
    """Handle adding a new book."""
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            description=form.description.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f'Book "{new_book.title}" added successfully!', 'success')
        return redirect(url_for('inventory'))
    return render_template('add_book.html', form=form)
=======

    if request.method == 'POST':

        try:

            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])


            new_book = Book(
                title=title,
                author=author,
                isbn=isbn,
                price=price,
                quantity=quantity
            )

            db.session.add(new_book)
            db.session.commit()

            flash(
                f"Book '{title}' added successfully!",
                "success"
            )

            return redirect(url_for('books'))

        except Exception as e:

            flash(
                f"Error adding book: {e}",
                "danger"
            )

            return redirect(url_for('add_book'))

    return render_template('add_book.html')
>>>>>>> 294f536 (Updated database models and barcode features)


@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """Handle editing a book."""
    book = Book.query.get_or_404(book_id)
    form = EditBookForm()
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.price = form.price.data
        book.description = form.description.data
        db.session.commit()
        flash(f'Book "{book.title}" updated successfully!', 'success')
        return redirect(url_for('inventory'))
    
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.price.data = book.price
        form.description.data = book.description
    
    return render_template('edit_book.html', form=form, book=book)


<<<<<<< HEAD
@app.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
=======
# --------------------------
# Delete Book
# --------------------------

@app.route('/delete_book/<int:book_id>')
>>>>>>> 294f536 (Updated database models and barcode features)
def delete_book(book_id):
    """Handle deleting a book."""
    book = Book.query.get_or_404(book_id)
    title = book.title
    db.session.delete(book)
    db.session.commit()
    flash(f'Book "{title}" has been deleted.', 'success')
    return redirect(url_for('inventory'))


<<<<<<< HEAD
@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')
=======
# --------------------------
# Barcode Generator
# --------------------------

@app.route('/generate_barcode/<int:book_id>')
def generate_barcode(book_id):

    book = Book.query.get_or_404(book_id)

    isbn = book.isbn

    code = barcode.get(
        'isbn13',
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

# --------------------------
# Checkout
# --------------------------
>>>>>>> 294f536 (Updated database models and barcode features)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form."""
    if request.method == 'POST':
<<<<<<< HEAD
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # In a real app, you would save this or send an email
        return render_template('contact.html', success=True, name=name)
    return render_template('contact.html')
=======

        try:

            book_id = int(
                request.form['book_id']
            )

            quantity = int(
                request.form['quantity']
            )

            book = Book.query.get(book_id)

            if book.quantity < quantity:

                flash(
                    "Not enough stock.",
                    "danger"
                )

                return redirect(
                    url_for('checkout')
                )

            subtotal = book.price * quantity

            tax = subtotal * 0.07

            total = subtotal + tax

            sale = Sale(

                book_id=book.id,

                quantity=quantity,

                subtotal=subtotal,

                tax=tax,

                total=total

            )

            db.session.add(sale)

            # Update inventory
            book.quantity -= quantity

            # Auto reorder
            if book.quantity <= 5:

                order = PurchaseOrder(

                    book_id=book.id,

                    quantity=10

                )

                db.session.add(order)

            db.session.commit()

            flash(
                "Sale completed!",
                "success"
            )

            return redirect(
                url_for('dashboard')
            )

        except Exception as e:

            flash(
                f"Error: {e}",
                "danger"
            )

            return redirect(
                url_for('checkout')
            )

    books = Book.query.all()

    return render_template(
        'checkout.html',
        books=books
    )
@app.route("/receipt/<int:sale_id>")
def receipt(sale_id):
>>>>>>> 294f536 (Updated database models and barcode features)

    sale = Sale.query.get_or_404(
        sale_id
    )

<<<<<<< HEAD
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404
=======
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
>>>>>>> 294f536 (Updated database models and barcode features)


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


# ==================== DATABASE INITIALIZATION ====================
def init_db():
    """Initialize the database with sample data."""
    with app.app_context():
        db.create_all()
        
        # Check if books already exist
        if Book.query.first() is None:
            sample_books = [
                Book(
                    title='The Great Gatsby',
                    author='F. Scott Fitzgerald',
                    price=12.99,
                    description='A classic novel of the Jazz Age.'
                ),
                Book(
                    title='To Kill a Mockingbird',
                    author='Harper Lee',
                    price=14.99,
                    description='A gripping tale of racial injustice and childhood innocence.'
                ),
                Book(
                    title='1984',
                    author='George Orwell',
                    price=13.99,
                    description='A dystopian novel about totalitarianism.'
                ),
                Book(
                    title='Pride and Prejudice',
                    author='Jane Austen',
                    price=11.99,
                    description='A romantic novel of manners and marriage.'
                ),
                Book(
                    title='The Catcher in the Rye',
                    author='J.D. Salinger',
                    price=13.99,
                    description='A story of teenage rebellion and alienation.'
                ),
            ]
            db.session.add_all(sample_books)
            db.session.commit()
        
        # Check if admin user exists
        if User.query.filter_by(username='admin').first() is None:
            admin_user = User(username='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()


if __name__ == '__main__':
    init_db()
    print('TEMPORARY TEST LINE')
    app.run(debug=True, host='127.0.0.1', port=5000)
