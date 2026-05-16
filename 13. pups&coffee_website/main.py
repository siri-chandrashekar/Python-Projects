from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

db = SQLAlchemy(app)

# -----------------------
# MODEL (Puppy)
# -----------------------
class Puppy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.String(50))
    description = db.Column(db.Text)
    story = db.Column(db.Text)
    image = db.Column(db.String(200))
    adoption_fee = db.Column(db.Float, default=0.0)


# -----------------------
# LOGIN
# -----------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# CREATE DB
with app.app_context():
    db.create_all()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')

        flash("Invalid credentials. Please try again.", "danger")
        return render_template("login.html")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')








@app.route('/')
def home():
    puppies = Puppy.query.all()
    return render_template('index.html', puppies = puppies)

@app.route('/puppy/<int:puppy_id>')
def puppy_detail(puppy_id):
    puppy = Puppy.query.get_or_404(puppy_id)
    return render_template('puppy_detail.html', puppy=puppy)

@app.route('/add-to-cart/<int:puppy_id>')
@login_required
def add_to_cart(puppy_id):
    cart = session.get('cart', {})

    if str(puppy_id) in cart:
        cart[str(puppy_id)] += 1
    else:
        cart[str(puppy_id)] = 1

    session['cart'] = cart

    return redirect(url_for('added_to_cart', puppy_id=puppy_id))

@app.route('/added-to-cart/<int:puppy_id>')
@login_required
def added_to_cart(puppy_id):
    puppy = Puppy.query.get_or_404(puppy_id)
    return render_template('added_to_cart.html', puppy=puppy)

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', {})
    
    puppies = []
    total = 0

    for puppy_id, quantity in cart.items():
        puppy = Puppy.query.get(int(puppy_id))
        if puppy:
            puppies.append({
                'puppy': puppy,
                'quantity': quantity
            })
            total += (puppy.adoption_fee or 0) * quantity

    return render_template('cart.html', puppies=puppies, total=total)


@app.route('/update-cart/<int:puppy_id>', methods=['POST'])
@login_required
def update_cart(puppy_id):
    cart = session.get('cart', {})
    quantity_raw = request.form.get('quantity', '1')

    try:
        quantity = int(quantity_raw)
    except ValueError:
        quantity = 1

    # If quantity is 0 or negative, remove the item from cart.
    if quantity <= 0:
        cart.pop(str(puppy_id), None)
    else:
        cart[str(puppy_id)] = min(quantity, 10)

    session['cart'] = cart
    flash("Cart updated.", "success")
    return redirect(url_for('cart'))

@app.route('/remove-from-cart/<int:puppy_id>')
def remove_from_cart(puppy_id):
    cart = session.get('cart', {})

    if str(puppy_id) in cart:
        cart.pop(str(puppy_id))

    session['cart'] = cart

    return redirect('/cart')

@app.route('/seed')
def seed():
    # Check if already seeded
    if Puppy.query.first():
        return "Already has data!"

    p1 = Puppy(
        name="Charlie",
        breed="Golden Retriever",
        age="2 months",
        description="Very playful and loves cuddles",
        story="Rescued from a rainy street, now loves people.",
        image="images/puppies/puppy1.jpg",
        adoption_fee=429.99
    )

    p2 = Puppy(
        name="Luna",
        breed="Indie",
        age="3 months",
        description="Calm and intelligent",
        story="Found near a temple, very gentle nature.",
        image="images/puppies/puppy2.jpg",
        adoption_fee=399.99
    )

    p3 = Puppy(
    name="Milo",
    breed="Beagle",
    age="4 months",
    description="Curious and energetic",
    story="Milo was found wandering near a busy street, constantly sniffing everything around him. Despite his rough start, he has an incredibly joyful spirit and loves exploring new spaces. He’s especially fond of children and will follow you around like your shadow.",
    image="images/puppies/puppy3.jpg",
    adoption_fee=599.99
    )

    p4 = Puppy(
    name="Bella",
    breed="Labrador",
    age="5 months",
    description="Loyal and affectionate",
    story="Bella was rescued from a small shelter where she was left behind. She has a calm and loving temperament, always seeking warmth and companionship. She enjoys quiet evenings and will happily rest beside you after a long day.",
    image="images/puppies/puppy4.jpg",
    adoption_fee=880.99
    )

    p5 = Puppy(
    name="Rocky",
    breed="German Shepherd",
    age="6 months",
    description="Alert and intelligent",
    story="Rocky comes from a rescue mission where he showed incredible resilience. Highly intelligent and quick to learn, he already responds to basic commands. He’s protective, brave, and will make a great companion for someone looking for a loyal friend.",
    image="images/puppies/puppy5.jpg",
    adoption_fee=540.39
    )

    db.session.add_all([p1, p2, p3, p4, p5])
    db.session.commit()

    return "Database seeded!"


@app.route('/checkout')
@login_required
def checkout():
    if not stripe.api_key:
        flash("Stripe key is missing. Set STRIPE_SECRET_KEY in your environment.", "danger")
        return redirect(url_for('cart'))

    cart = session.get('cart', {})

     # If cart is empty → redirect
    if not cart:
        flash("Your cart is empty 🐾 Add a puppy first!", "warning")
        return redirect(url_for('cart'))
    line_items = []

    for puppy_id, quantity in cart.items():
        puppy = Puppy.query.get(int(puppy_id))

        if puppy:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': puppy.name,
                    },
                    'unit_amount': int((puppy.adoption_fee or 0) * 100),
                },
                'quantity': quantity,
            })

    session_checkout = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:5000/success',
        cancel_url='http://127.0.0.1:5000/cart',
    )

    return redirect(session_checkout.url)

@app.route('/success')
@login_required
def success():
    session.pop('cart', None)
    return "🎉 Adoption successful! You earned a free coffee ☕"


if __name__ == '__main__':
    app.run(debug=True)
