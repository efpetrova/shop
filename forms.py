from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, IntegerField, DateField
import datetime
from wtforms.validators import Length,DataRequired
from wtforms.widgets import HiddenInput

class OrderForm(FlaskForm):
    name = StringField('Ваше имя', [Length(min=3)])
    address = StringField('Ваш адрес', [Length(min=3)])
    email = StringField('Электропочта', [Length(min=3)])
    phone = StringField('Ваш телефон', [Length(min=9)])
    date_now = DateField('date', widget=HiddenInput(), default=datetime.datetime.now)
    status = BooleanField('true',widget=HiddenInput(), default=True)
    lst_dishes = StringField('dishes', [Length(min=3)], widget=HiddenInput())
    user_id = IntegerField('user_id', widget=HiddenInput())
    sum = IntegerField('sum', widget=HiddenInput())

class RegistrationForm(FlaskForm):
    email = StringField('Электропочта', [Length(min=3)])
    password = StringField('Пароль', [Length(min=5)])

class LoginForm(FlaskForm):
    email = StringField('Электропочта', [Length(min=3)])
    password = StringField('Пароль', [Length(min=5)])