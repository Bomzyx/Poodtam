import datetime
import mongoengine as me
import markdown

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    current_app,
    send_file,
    abort,
    flash,
)
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

from poodtam import models
from .. import oauth
from .. import forms

module = Blueprint("accounts", __name__)


@module.route("/register", methods=["GET", "POST"])
def register():
    form = forms.accounts.RegistrationForm()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template("accounts/register.html", form=form)

    if oauth.create_user(form):
        flash("Account created successfully.", "success")
        return redirect(url_for("accounts.login"))
    flash("This username already exists.", "danger")
    return "Failed."


@module.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = forms.accounts.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = models.User.objects(username=username).first()
        if user and oauth.handle_authorized_user(form):
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("accounts/login.html", form=form)


@module.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()

    return redirect(url_for("dashboard.index"))
