from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user

from .import db
import json


views = Blueprint("views", __name__)

@views.route("/home", methods=["GET","POST"])
@views.route("/", methods=["GET","POST"])

def home():
    
    return render_template('home.html')