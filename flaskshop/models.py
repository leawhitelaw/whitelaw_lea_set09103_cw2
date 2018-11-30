from flaskshop import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#~ ~ ~ ~ ~ ~ ~ define clothing model for data ~ ~ ~ ~ ~
class Clothing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    colour = db.Column(db.String(20), nullable=False)
    brand = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    clothing_category = db.Column(db.String(20), nullable=False)
    sub_category = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String(30), nullable = False)
    colour_two = db.Column(db.String(20))
    image_two = db.Column(db.String(30))
    colour_three = db.Column(db.String(20))
    image_three = db.Column(db.String(30))

    def __init__(self, name, colour, brand, size, price, clothing_category, sub_category, gender, image_file, colour_two, image_two, colour_three, image_three):
        self.name = name
        self.colour = colour
        self.brand = brand
        self.size = size
        self.price = price
        self.clothing_category = clothing_category
        self.sub_category = sub_category
        self.gender = gender
        self.image_file = image_file
        self.colour_two = colour_two
        self.image_two = image_two
        self.colour_three = colour_three
        self.image_three = image_three

    def __repr__(self):
        return '<Clothing %r>' %self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favourites_boards = db.relationship('Favourites_board', backref = 'creator', lazy=True)

    def __repr__(self):
        return '<User %r>' %self.email

class Favourites_relationship(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    clothing_id = db.Column(db.Integer, db.ForeignKey('clothing.id'),nullable=False)
    board_title = db.Column(db.Unicode, db.ForeignKey('favourites_board.title'), nullable=False)

class Favourites_board(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favourites_relationships = db.relationship('Favourites_relationship', backref='favs_board', lazy=True)

    def __repr__(self):
        return '<Favourites_board %r>' %self.title
