import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This connects to your PostgreSQL database you set up on Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Part 1 Infrastructure: The Database Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))

# Create the database and add sample products
with app.app_context():
    db.create_all()
    if not Product.query.first():
        p1 = Product(name="Cloud Laptop", price="$1200", description="High performance for AI tasks.")
        p2 = Product(name="Wireless Mouse", price="$45", description="Ergonomic cloud-sync mouse.")
        p3 = Product(name="Gaming Keyboard", price="$150", description="Mechanical RGB keyboard.")
        db.session.add_all([p1, p2, p3])
        db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)