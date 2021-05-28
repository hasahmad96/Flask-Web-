from flask import render_template, Flask, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask Instance
app = Flask(__name__)
# Add Database
#SQLit DB
#app.config['SQLALCHEMY_DATABASE_UR'] = 'sqlite:///users.db'
#MYSQL DB
app.config['SQLALCHEMY_DATABASE_UR'] = 'mysql+pymysql://root:aimsol123@localhost/db_name/users'
#initialize the database
db = SQLAlchemy(app)
#secret key
app.config['SECRET_KEY'] = "my secret key "

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name
db.create_all()
db.session.commit()

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
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