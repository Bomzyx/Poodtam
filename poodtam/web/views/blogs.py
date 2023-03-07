from flask import Blueprint, render_template_string, render_template, redirect, url_for

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
    blog.last_updated_date = datetime.datetime.now()
    blog.save()

    return redirect(url_for('dashboard.index'))


