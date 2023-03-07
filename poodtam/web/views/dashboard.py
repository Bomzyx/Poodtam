from flask import Blueprint, render_template
from ... import models
from .. import forms

module = Blueprint("dashboard", __name__, url_prefix="/")


@module.route("/")
def index():
    blogs = models.Blog.objects().order_by("-created_date")
    comment_form = forms.blogs.CommentForm()

    return render_template(
        "/dashboard/index.html", blogs=blogs, comment_form=comment_form
    )
