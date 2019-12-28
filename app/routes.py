import re

from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import LoginForm, RegistrationForm, InventoryRemove, InventoryAdd
from flask_login import current_user,login_user, logout_user, login_required
from app.models import User,Inventory
from flask import request
from werkzeug.urls import url_parse

from app.utils.amz_data_handler import AmzHandler,URLS

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/inventory_upload')
@login_required
def inventory_upload():
    return render_template('inventory_upload.html')

@app.route('/postinventory', methods = ['POST'])
def postinventory():
    jsdata = request.form['data']
    user = User.query.filter_by(username=current_user.username).first()
    print(jsdata)
    for line in jsdata.split('|'):
        elem = line.split(',')
        i = Inventory(source=elem[0],item=elem[1],price=float(elem[2]),user_id=int(user.id))
        db.session.add(i)
    db.session.commit()
    return('done')

@app.route('/showinventory', methods=['GET','POST'])
@login_required
def inventory_grid():
    user = User.query.filter_by(username=current_user.username).first()

    remove_form = InventoryRemove()
    if remove_form.validate_on_submit():
        item_code = remove_form.item_code.data
        item = Inventory.query.filter_by(id=item_code).first()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('inventory_grid'))

    add_form = InventoryAdd()
    if add_form.validate_on_submit():
        source = add_form.source.data
        item = add_form.name.data
        price = add_form.price.data
        i = Inventory(source=source,item=item,price=float(price),user_id=int(user.id))
        db.session.add(i)
        db.session.commit()
        return redirect(url_for('inventory_grid'))

    items = Inventory.query.filter_by(user_id=user.id).all()
    if len(items):
        records = []
        for item in items:
            records.append((item.id,item.source,item.item,item.price))
    else:
        records = [(0,'tbd','tbd',0)]
    return render_template('product_table.html',records=records, remove_form = remove_form, add_form=add_form)

@app.route('/showamzdashboard', methods=['GET','POST'])
@login_required
def amz_dashboard():
    records = []
    a = AmzHandler('BATH_OILS',URLS['BATH_OILS'])
    bestsellers = a.getBestSellers()
    results = a.processBestSellers(bestsellers)
    for result in results:
        records.append((result['current_rank'],re.compile("[-,]").split(result['name'])[0],result['current_price'],result['link']))
    return render_template('amz_dashboard.html',records=records)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)