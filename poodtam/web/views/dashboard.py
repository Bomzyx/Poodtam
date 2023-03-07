from flask import Blueprint, render_template
from ... import models
module = Blueprint("dashboard", __name__, url_prefix="/")


@module.route("/")
def index():
    blogs = models.Blog.objects()

    return render_template("/dashboard/index.html", blogs=blogs)
