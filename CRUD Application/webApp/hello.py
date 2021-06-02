#everything should be installed in virtual env in git bash prompt
from flask import render_template, Flask, flash, request
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz  # 3rd party: $ pip install pytz

from flask_migrate import Migrate
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# Create Flask Instance
app = Flask(__name__)
# Add Database
#SQLit DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#MYSQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aimsol123@localhost/users'

#secret key
app.config['SECRET_KEY'] = "my secret key "

#initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    #flask integration
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Karachi')))

    #Create a String -------- put name on the screen
    def __repr__(self):
        return '<Name %r>' % self.name
#db.create_all()
#db.session.commit()
'''
in gitbash terminal 
winpty python
from <filename> import db
db.create_all()
exit()
'''

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                               name=name,
                               form=form,
                               our_users=our_users)

    except:
        flash("oopps, there was an error deleting the user")
        return render_template("add_user.html",
                               name=name,
                               form=form,
                               our_users=our_users)

class UserForm(FlaskForm):
    name = StringField("Writ your name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

#update db records
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("update.html",
                                   form=form,
                                   name_to_update = name_to_update)
        except:
            flash("Error! Looks like there was a problem .... Try again")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)

    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               id = id)

# create a Form Class (first make secret key)
class NamerForm(FlaskForm):
    name = StringField("What's yout name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

    #BooleanField, DateField, DateTimeField, DecimalField, FileField, HiddenField
    #MultipleField, FieldList, FloatField, FormField, IntegerField, PasswordField
    #RadioField, SelectField, SelectMultipleField, SubmitField, StringField, TextAreaField

    ##Validators
    #DataRequired, Email, EqualTo, InputRequired, IPAddress, Length, MacAddress, NumberRange
    #Optional, Regexp, URL, UUID, AnyOf, NoneOf
# priniting with jinja

# FILTERS !!!!
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color = form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
        form.favorite_color.data=''

        flash("User added successfully.")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           name=name,
                           form=form,
                           our_users=our_users)

@app.route('/')
def index():
    first_name = "Hasan"
    stuff = "This is bold text."

    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41.5, "civic"]
    return render_template("index.html",
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza = favorite_pizza)


#127.0.0.1:5000/user/hasan
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# end # priniting with jinja

# custom error pages

# 1. Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# 2. Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
# end custom error page

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")
    return render_template("name.html",
                           name = name,
                           form = form)

if __name__ == "__main__":
    app.run(debug=True)