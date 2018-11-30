from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

############ init flask app #################
app = Flask(__name__)

############# config app ###################
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///var/shop.db'
app.config['SECRET_KEY'] = 'xe5BfCx93xa5bxe4xc2x1fx82Dxf8ax0bA'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskshop import routes
