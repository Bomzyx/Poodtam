from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_mongoengine.wtf import model_form

from poodtam import models

BaseRegistrationForm = model_form(
    models.User,
    FlaskForm,
    exclude=[
        "email",
        "picture",
        "roles",
        "created_date",
        "updated_date",
        "is_active",
        "last_login_date",
    ],
    field_args={
        "username": {"label": "ชื่อบัญชีผู้ใช้"},
        "name": {"label": "ชื่อ"},
    },
)


class RegistrationForm(BaseRegistrationForm):
    password = fields.PasswordField(
        "รหัสผ่าน",
        validators=[validators.DataRequired(), validators.EqualTo("password")],
    )
    confirm_password = fields.PasswordField(
        "ยืนยันรหัสผ่าน",
        validators=[validators.DataRequired(), validators.EqualTo("password")],
    )
    email = fields.StringField(
        "อีเมล", validators=[validators.Email(), validators.Optional()]
    )


# Define the user login form
class LoginForm(FlaskForm):
    username = fields.StringField(
        "ชื่อบัญชีผู้ใช้", validators=[validators.DataRequired()]
    )
    password = fields.PasswordField("รหัสผ่าน", validators=[validators.DataRequired()])
    submit = fields.SubmitField("ล็อคอิน")


BaseProfileForm = model_form(
    models.User,
    FlaskForm,
    field_args={
        "name": {"label": "ชื่อ"},
        "email": {"label": "อีเมล"},
    },
    exclude=[
        "username",
        "password",
        "created_date",
        "updated_date",
        "is_active",
        "last_login_date",
    ],
)


class ProfileForm(BaseProfileForm):
    email = fields.StringField(
        "อีเมล", validators=[validators.Email(), validators.Optional()]
    )
