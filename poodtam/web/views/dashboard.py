from flask import Blueprint, render_template, request
from ... import models
from .. import forms

module = Blueprint("dashboard", __name__, url_prefix="/")


TAG_CHOCIES = [
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


@module.route("/")
def index():
    blogs = models.Blog.objects().order_by("-created_date")
    comment_form = forms.blogs.CommentForm()
    tag_choices = [t[1] for t in TAG_CHOCIES]
    return render_template(
        "/dashboard/index.html",
        blogs=blogs,
        comment_form=comment_form,
        tag_choices=tag_choices,
        filter_tag=request.args.get("filter_tag"),
    )
