from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_mongoengine.wtf import model_form

from poodtam import models


TAG_CHOICES = [
    ("life", "ปัญหาชีวิต"),
    ("love", "ความรัก"),
    ("food", "อาหาร"),
    ("animal", "สัตว์"),
    ("pet", "สัตว์เลี้ยง"),
    ("car", "ยานพาหนะ"),
    ("mobile", "โทรศัพท์"),
    ("computer", "คอมพิวเตอร์"),
    ("technology", "เทคโนโลยี"),
    ("cloud", "คลาวด์"),
    ("study", "การศึกษา"),
]

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
    tags = fields.SelectMultipleField("แท็ก", choices=TAG_CHOICES)


BaseCommentForm = model_form(
    models.Comment,
    FlaskForm,
    exclude=["owner", "created_date", "last_updated_date", "body"],
)


class CommentForm(BaseCommentForm):
    body = fields.TextAreaField(validators=[validators.InputRequired()])
