from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    return render_template("login.html", boolean=True)

@auth.route('/lougout')
def logout():
    return "<p>Logout</p>"

@auth.route('/signup')
def sign_up():
     return render_template("sign_up.html")

@auth.route('/order')
def order():
     return render_template("order.html")

@auth.route('/menu')
def menu():
     return render_template("menu.html")
