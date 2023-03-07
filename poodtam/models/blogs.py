import mongoengine as me
import datetime
import markdown

class Blog(me.Document):
    meta = {"collection": "blogs"}

    subject = me.StringField(required=True, max_length=255)
    body = me.StringField(required=True)

    owner = me.ReferenceField("User", dbref=True, required=True)

    created_date = me.DateTimeField(required=True)
    last_updated_date = me.DateTimeField(required=True)

    def get_body(self):
        return markdown.markdown(self.body)

