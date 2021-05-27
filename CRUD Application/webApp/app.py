from flask import render_template, request, jsonify, Flask, flash
import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key "

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