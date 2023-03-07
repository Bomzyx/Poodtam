from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_mongoengine.wtf import model_form

from poodtam import models

BaseBlogForm = model_form(
    models.Blog,
    FlaskForm,
    exclude=[
        "owner",
        "created_date",
        "last_updated_date",
    ],
    field_args={
        "subject": {"label": "หัวข้อ"},
        "body": {"label": "เนื้อหา"},
    },
)


class BlogForm(BaseBlogForm):
    pass