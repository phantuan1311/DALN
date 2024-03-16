from re import template
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, get_flashed_messages
from sqlalchemy.sql.expression import false
from manage.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from manage import db
from sqlalchemy import or_

user = Blueprint("user", __name__)

@user.route("/login_custumer", methods=["GET", "POST"])
def login_cus():
    if request.method == "POST":
        data = request.form.get("data")
        customer_password = request.form.get("customer_password")
        if "@" in data:
             email = data
             user_name = None
        else:
            user_name = data
            email = None
        
        if email:
            user = User.query.filter_by(email=email).first()      
        elif user_name:
            user = User.query.filter_by(user_name=user_name).first()
        
        if user:
            if check_password_hash(user.customer_password, customer_password):
                session.permanent = True     
                login_user(user, remember=True)
                flash("Logged in successfully!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Invalid username or password", "error")
        else:
            flash("Người dùng không tồn tại", "error")
    messages = get_flashed_messages()
    return render_template("login_cus/login_customer.html", user=current_user)



@user.route("/signup",methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        phone_number=request.form.get("phone_number")
        customer_password = request.form.get("customer_password")
        confirm_password = request.form.get("confirm_password")
        user = User.query.filter_by(email = email).first()
        if user:
            flash("User existed !", category="error")
        elif len(email) < 13:
            flash("Email sort !", category="error")
        elif len(customer_password) < 7:
            flash("Password sort !",category="error")
        elif customer_password != confirm_password:
            flash("Password does not match !",category="error")
        else:
            customer_password = generate_password_hash(customer_password, method="scrypt")
            new_user = User(email=email,user_name=user_name, phone_number=phone_number, customer_password=customer_password)
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user,remember=True)
                flash("User created !", category="success")
                return redirect(url_for("views.home"))
            except:
                "error"
    messages = get_flashed_messages()
    return render_template("login_cus/signup.html", user=current_user)