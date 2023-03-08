from flask import (
    Blueprint,
    render_template_string,
    render_template,
    redirect,
    url_for,
    request,
)

from .. import forms
from ... import models

from flask_login import current_user, login_required

import datetime

module = Blueprint("blogs", __name__, url_prefix="/blogs")


@module.route(
    "/create",
    methods=["GET", "POST"],
    defaults={"blog_id": None},
)
@module.route("/<blog_id>/edit", methods=["GET", "POST"])
@login_required
def create_or_edit(blog_id):
    form = forms.blogs.BlogForm()

    blog = None
    if blog_id:
        blog = models.Blog.objects.get(id=blog_id)
        form = forms.blogs.BlogForm(obj=blog)

    if not form.validate_on_submit():
        return render_template("/blogs/create-or-edit.html", form=form, blog=blog)

    if not blog_id:
        blog = models.Blog()
        blog.owner = current_user._get_current_object()
        blog.created_date = datetime.datetime.now()

    blog.subject = form.subject.data
    blog.body = form.body.data
    blog.tags = [t for t in form.tags.data]
    blog.last_updated_date = datetime.datetime.now()
    blog.save()

    return redirect(url_for("dashboard.index"))


@module.route(
    "/comments/<comment_id>/comment",
    methods=["GET", "POST"],
    defaults={"blog_id": None},
)
@module.route(
    "/<blog_id>/comment",
    methods=["GET", "POST"],
    defaults={"comment_id": None},
)
@login_required
def comment(blog_id, comment_id):
    form = forms.blogs.CommentForm()

    if not form.validate_on_submit():
        return redirect(url_for("dashboard.index"))

    comment = models.Comment(
        body=form.body.data,
        owner=current_user._get_current_object(),
        last_updated_date=datetime.datetime.now(),
        created_date=datetime.datetime.now(),
    )
    comment.save()
    if blog_id:
        target_blog = models.Blog.objects.get(id=blog_id)
        target_blog.comments.append(comment)
        target_blog.save()

    if comment_id:
        target_comment = models.Comment.objects.get(id=comment_id)
        target_comment.comments.append(comment)
        target_comment.save()

    return redirect(url_for("dashboard.index"))


@module.route(
    "/comments/<comment_id>/liked",
    methods=["GET", "POST"],
    defaults={"blog_id": None},
)
@module.route(
    "/<blog_id>/liked",
    methods=["GET", "POST"],
    defaults={"comment_id": None},
)
@login_required
def like_target(blog_id, comment_id):
    user = current_user._get_current_object()

    blog_target = None
    if blog_id:
        blog_target = models.Blog.objects.get(id=blog_id)
        if not user in blog_target.liked_by:
            blog_target.liked_by.append(user)
        else:
            blog_target.liked_by.remove(user)
        blog_target.save()

    comment_target = None
    if comment_id:
        comment_target = models.Comment.objects.get(id=comment_id)
        if not user in comment_target.liked_by:
            comment_target.liked_by.append(user)
        else:
            comment_target.liked_by.remove(user)
        comment_target.save()

    total_like = len(blog_target.liked_by) if blog_id else len(comment_target.liked_by)
    return dict({"total_like": total_like})


@module.route("/<blog_id>")
@login_required
def view(blog_id):
    blog = models.Blog.objects.get(id=blog_id)
    comment_form = forms.blogs.CommentForm()
    tag_choices = [t[1] for t in TAG_CHOCIES]

    return render_template(
        "blogs/view.html", blog=blog, comment_form=comment_form, tag_choices=tag_choices
    )


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


@module.route("/view_liked_post")
@login_required
def view_liked():
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

    blogs = [b for b in blogs if current_user._get_current_object() in b.liked_by]

    return render_template(
        "/dashboard/index.html",
        blogs=blogs,
        comment_form=comment_form,
        tag_choices=tag_choices,
        filter_tag=request.args.get("filter_tag"),
        sorted_by=sorted_by,
    )
