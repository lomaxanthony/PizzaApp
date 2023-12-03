from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import User, Orders
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import requests


auth = Blueprint('auth', __name__)

@auth.route('/home')


@auth.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
          email = request.form.get('email')
          password = request.form.get('password')

          user = User.query.filter_by(email=email).first()
          if user:
               if check_password_hash(user.password, password):
                   flash('Logged in successfully!', category='success')
                   login_user(user, remember=True)
                   return redirect(url_for('views.home'))
               else:
                    flash('Incorrect password, try again.', category='error')
          else:
               flash('Email does not exist.', category='error')
               
     return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.menu'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
     if request.method == 'POST':
          email = request.form.get('email')
          first_name = request.form.get('firstName')
          last_name = request.form.get('lastName')
          phone_number = request.form.get('phoneNumber')
          address = request.form.get('address')
          password1 = request.form.get('password1')
          password2 = request.form.get('password2')

          user = User.query.filter_by(email=email).first()
          if user:
               flash('Email already exists.', category='error')
          elif len(email) < 4:
               flash('Email must be greater than 4 characters.', category='error')
          elif len(first_name) and len(last_name) < 2:
               flash('First name must be greater than 1 character.', category='error')
          elif len(phone_number) != 10:
               flash('Not a valid phone number', category='error')
          elif password1 != password2:
               flash("Passwords don't match.", category='error')
          elif len(password1) < 7:
               flash('Password must be at least 7 characters.', category='error')
          else:
               new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
               db.session.add(new_user)
               db.session.commit()
               login_user(new_user, remember=True)
               flash('Account created!', category='success')
               return redirect(url_for('views.home'))

     return render_template("sign_up.html", user=current_user)

# @auth.route('/place_order', methods=['GET', 'POST'])
# @login_required
# def place_order():
#     if request.method == 'POST':
#         order_data = request.form.get('order_data')

#         new_order = Orders(data=order_data, user=current_user)

#         db.session.add(new_order)
#         db.session.commit()

#         flash('Order placed successfully!', category='success')

#         return redirect(url_for('auth.order_confirmation'))

    
#    return render_template("order.html", user=current_user)

@auth.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
     if request.method == 'POST':
          pizza_size = request.form.get('pizza_size')
          toppings = request.form.getlist('toppings')

          pizza_price = calculate_price(pizza_size, toppings)

          new_pizza_order = Orders(
               pizza_size=pizza_size,
               pizza_price=pizza_price,
               user=current_user,
               toppings=toppings
        )


          db.session.add(new_pizza_order)
          db.session.commit()

          flash('Pizza successfully added to cart!', category='success')

          return redirect(url_for('auth.order'))


@auth.route('/cart')
@login_required
def cart():
     user_cart = Orders.query.filter_by(user=current_user).all()
     return render_template('cart.html', user=current_user, user_cart=user_cart)


def calculate_price(size, toppings):
               if size == 'Large':
                    p = 18
                    x = len(toppings) * 1.5
                    total_price = p + x
               elif size == 'Medium':
                    p = 16
                    x = len(toppings) * 1.5
                    total_price = p + x
               else:
                    p = 14
                    x = len(toppings) * 1.5
                    total_price = p + x

               return str(total_price)


@auth.route('/order', methods=['GET', 'POST'])
@login_required
def order():
     return render_template("order.html", user=current_user)


@auth.route('/menu')
def menu():
     return render_template("menu.html", user=current_user)

@auth.route('/place_order')
@login_required
def place_order():
     user_cart = Orders.query.filter_by(user=current_user).all()
     for cart_item in user_cart:
          db.session.delete(cart_item)
     db.session.commit()
     return render_template('success.html', user=current_user)

@auth.route('/clear_cart')
@login_required
def clear_cart():
     user_cart = Orders.query.filter_by(user=current_user).all()
     for cart_item in user_cart:
          db.session.delete(cart_item)
     db.session.commit()
     return render_template('cart.html', user=current_user)


@auth.route('/avg_cart')
@login_required
def avg_cart():
     user_cart = Orders.query.filter_by(user=current_user).all()
     x = 0
     p = 0
     for item in user_cart:
          x += 1
          p += float(item.pizza_price)
     

     url = "http://127.0.0.1:8001/price_average/{}/{}"

     order_total = str(p)
     amount_ordered = x
     
     rep = requests.get(url.format(order_total, amount_ordered))
     
     flash(f'{rep.json()}', category='info')
     print(rep.json())
     return render_template('cart.html', user=current_user, user_cart=user_cart)

     

