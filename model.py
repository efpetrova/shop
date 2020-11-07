import csv, random, json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from collections import Counter


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    orders = db.relationship("Order", back_populates="user")

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.String)
    status = db.Column(db.Boolean)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    lst_dishes = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user= db.relationship("User")
    name = db.Column(db.String)
    date_now = db.Column(db.DateTime)

    def get_meals(self):
        lst_dishes = json.loads(self.lst_dishes)
        meals =db.session.query(Meal).filter(Meal.id.in_(lst_dishes)).all()
        counter = Counter(lst_dishes)
        return [ (m, counter[m.id]) for m in meals]


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    meals = db.relationship("Meal", uselist=True)

    def random_meals(self):
        return random.sample(self.meals,3)


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Category")

    def _price(self):
        return int(self.price)

def reload_data():
    with open('categories.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            category = Category(id=row[0], title=row[1])
            db.session.add(category)
        db.session.commit()

    with open('meals.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            meal = Meal(id=row[0], title=row[1], price=row[2], description=row[3], picture=row[4], category_id=row[5])
            db.session.add(meal)
        db.session.commit()


if __name__ == '__main__':
    reload_data()

