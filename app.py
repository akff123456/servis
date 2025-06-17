from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from models import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    category = request.form['category']
    quantity = int(request.form['quantity'])
    purchase_price = float(request.form['purchase_price'])
    sale_price = float(request.form['sale_price'])
    new_product = Product(name=name, category=category, quantity=quantity,
                          purchase_price=purchase_price, sale_price=sale_price)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.name = request.form['name']
    product.category = request.form['category']
    product.quantity = int(request.form['quantity'])
    product.purchase_price = float(request.form['purchase_price'])
    product.sale_price = float(request.form['sale_price'])
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
