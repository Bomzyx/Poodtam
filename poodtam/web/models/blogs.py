import mongoengine as me
import datetime


class Blog(me.Document):
    meta = {"collection": "blogs"}

    subject = me.StringField(required=True)
    body = me.StringField(required=True)
