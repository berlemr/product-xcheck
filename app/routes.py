from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/products')
def product_grid():
    # user = {'username': 'Miguel'}
    # return render_template('index.html', title='Home', user=user)
    records = [('a',1),('b',2),('c',3)]
    return render_template('product_table.html',records=records)