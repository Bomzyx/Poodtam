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
    blogs = models.Blog.objects()
    comment_form = forms.blogs.CommentForm()
    tag_choices = [t[1] for t in TAG_CHOCIES]

    sorted_by = request.args.get("sorted_by")

    if sorted_by == "most_liked":
        blogs = sorted(blogs, key=lambda x: len(x.liked_by), reverse=True)

    elif sorted_by == "least_liked":
        blogs = sorted(blogs, key=lambda x: len(x.liked_by))

    elif sorted_by == "most_comment":
        blogs = sorted(blogs, key=lambda x: x.count_comment(), reverse=True)

    elif sorted_by == "least_comment":
        blogs = sorted(blogs, key=lambda x: x.count_comment())

    elif sorted_by == "oldest_date":
        blogs = blogs.order_by("created_date")
    else:
        blogs = blogs.order_by("-created_date")

    return render_template(
        "/dashboard/index.html",
        blogs=blogs,
        comment_form=comment_form,
        tag_choices=tag_choices,
        filter_tag=request.args.get("filter_tag"),
        sorted_by=sorted_by,
    )
