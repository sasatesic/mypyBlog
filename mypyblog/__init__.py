from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '0f09e1140b30fe461c49a69e0ce27b64'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'korisnici.login'
login_manager.login_message = "Morate se ulogovati da bi pristupili svom profilu!"
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mojpyblogrs@gmail.com'
app.config['MAIL_PASSWORD'] = 'yneucacshbypeaai'
mail = Mail(app)

from mypyblog.korisnici.routes import korisnici
from mypyblog.postovi.routes import postovi
from mypyblog.main.routes import main

app.register_blueprint(korisnici)
app.register_blueprint(postovi)
app.register_blueprint(main)