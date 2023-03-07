import mongoengine as me
import datetime


class User(me.Document):
    meta = {"collection": "users", "strict": False}

    username = me.StringField(required=True)
    password = me.BinaryField(required=True)

    name = me.StringField(required=True)
    description = me.StringField()
    picture = me.ImageField(thumbnail_size=(800, 600, True))

    roles = me.ListField(me.StringField(), default=["user"])

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)
