from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY']='5f65f191c38f48f2480683949927f192'
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///DB.db'
db=SQLAlchemy(app)
login=LoginManager(app)
bcrypt=Bcrypt(app)

# these messages for account page
login.login_view='login'
login.login_message_category='info'


@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors/500.html'), 500



from FlaskCRUD import routes
