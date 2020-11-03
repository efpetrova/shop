from flask import Flask, render_template, session, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from collections import Counter
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,DateTimeField,IntegerField
from wtforms.validators import Length,DataRequired
from wtforms.widgets import HiddenInput
from hashlib import md5
import uuid
from model import *

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
#db = SQLAlchemy(app)

# app & db got imported from model.py

app.secret_key = uuid.uuid4().hex
#migrate = Migrate(app, db)

user = User(password="test", email="test@gmail.com")
db.session.add(user)
db.session.commit()

@app.before_request
def find_or_create_cart():
    if "cart" not in session:
        session['cart'] = []

@app.before_request
def find_or_create_user():
    if 'user_id' not in session:
        session['user_id'] = None

@app.route('/')
def main():
    categories = db.session.query(Category).all()
    return render_template('main.html', categories=categories)

def lst_goods():
    for i in range(len(session['cart'])):
        meal = db.session.query(Meal).filter(Meal.id == session.get('cart')[i]).all()
    return meal

@app.route('/add_to_cart/<int:item>/', methods=['GET'])
def add_to_cart(item):
    cart = session['cart']
    cart.append(item)
    session['cart'] = cart
    return redirect('/cart/')

@app.route('/delete_cart/<int:id>/')
def delete_cart(id):
    session['cart'].remove(id)
    session.modified = True
    flash('Блюдо удалено из корзины')
    return redirect('/cart/')


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [Length(min=3)])
    address = StringField('Ваш адрес', [Length(min=3)])
    email = StringField('Электропочта', [Length(min=3)])
    phone = StringField('Ваш телефон', [Length(min=9)])
    date = StringField('date', widget=HiddenInput(), default='22.10.20')
    status = BooleanField('true',widget=HiddenInput(), default=True)
    lst_dishes = StringField('dishes', [Length(min=3)], widget=HiddenInput())
    user_id = IntegerField('user_id', widget=HiddenInput())
    sum = IntegerField('sum', widget=HiddenInput())


@app.route('/order_done/', methods=['POST'])
def order_done():
    order_form = OrderForm()
    def _create_order(form):
        order = Order()
        form.populate_obj(order)
        db.session.add(order)
        db.session.commit()

    if order_form.validate_on_submit():
        _create_order(order_form)
        return render_template('ordered.html')
    else:
        meals, counter, sum = order_state(session)
        return render_template('cart.html', form=order_form, goods=session['cart'], meals=meals, counter=counter, sum=sum, user_id=session['user_id'])

def order_state(session):
    meals = db.session.query(Meal).filter(Meal.id.in_(session.get('cart'))).all()
    counter = Counter(session.get('cart'))
    return meals, counter, sum([counter[i.id] * int(i.price) for i in meals])

@app.route('/cart/', methods=['GET'])
def cart():
    meals, counter, sum= order_state(session)
    order_form = OrderForm(data={'lst_dishes': session.get('cart'), 'sum': sum, "user_id": session['user_id']})
    return render_template('cart.html', form=order_form, goods=session['cart'], meals=meals, counter=counter, sum=sum, user_id=session['user_id'])


@app.route('/account/')
def account():
    return render_template('account.html')

class LoginForm(FlaskForm):
    email = StringField('Электропочта', [Length(min=3)])
    password = StringField('Пароль', [Length(min=5)])

@app.route('/login/', methods=["GET"])
def login():
    login_form=LoginForm()
    return render_template('login.html', form=login_form)

@app.route('/login_done/', methods=["POST"])
def login_done():
    login_form = LoginForm()
    # Если форма не валидна
    #if not loginForm.validate_on_submit():
    #    return render_template("login.html", form=loginForm)

    hash_password = md5(login_form.password.data.encode())  # Преобразуем в байтовую строку
    password = hash_password.hexdigest()

    user = User.query.filter(User.email == login_form.email.data).first()
    if not user or user.password != password:
        error_msg = "Не указано имя или электронная почта"
        return redirect("/login/")
    else:
        session["user_id"] = user.id
        session["email"] = user.email

    return redirect("/cart")

class RegistrationForm(FlaskForm):
    email = StringField('Электропочта', [Length(min=3)])
    password = StringField('Пароль', [Length(min=5)])

@app.route('/register/', methods=['GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route('/register_done/', methods=['POST'])
def register_done():
    register_form = RegistrationForm()
    user = User()
    user.email = register_form.email.data
    user.password = md5(register_form.password.data.encode()).hexdigest()

    if not user or not user.email:
        error_msg = "Не указано имя или электронная почта"
        return render_template("register.html", error_msg=error_msg)

    db.session.add(user)
    db.session.commit()
    return redirect("/cart")


@app.route('/logout', methods=["GET"])
def logout():
    if session.get("user_id"):
        session.pop("user_id")
    return redirect("/login")

if __name__ == '__main__':
    app.run()
