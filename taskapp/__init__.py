from flask import Flask
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

bcrypt = Bcrypt(app)

db_connection = mysql.connector.connect(
    host="35.233.227.191",
    user="aimee",
    passwd="HJ4cGd4#`[M}5B($",
    database="final_project"
)
db_cursor = db_connection.cursor()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from taskapp import routes
