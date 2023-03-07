import mongoengine as me
import datetime
import markdown
import humanize

def change_suffix_time_to_thai(time):
    return time.replace(
                'ago', 'ที่ผ่านมา'
            ).replace(
                'now', 'ตอนนี้'
            ).replace(
                'a minute ', 'ไม่กี่นาที'
            ).replace(
                'minutes ', 'นาที'
            ).replace(
                'hours ', 'ชั่วโมง'
            ).replace(
                'days ', 'วัน' 
            ).replace(
                'months ', 'เดือน'
            ).replace(
                'years ', 'ปี'
            ).replace(
                'year,', 'ปี'
            )

class Comment(me.Document):
    meta = {"collection": "comments"}

    body = me.StringField(required=True)
    owner = me.ReferenceField("User", dbref=True, required=True)
    created_date = me.DateTimeField(required=True)
    last_update_date = me.DateTimeField(required=True)
    
    liked_by = me.ListField(me.ReferenceField("User", dbref=True))
    comments = me.ListField(me.ReferenceField("Comment", dbref=True))

    def get_body(self):
        return markdown.markdown(self.body)
    
    def get_natural_last_updated_date(self):
        return self.last_updated_date.strftime("%d %B %Y, %I:%M %p")
    
    def get_natural_created_date(self):
        return self.created_date.strftime("%d %B %Y, %I:%M %p")

    def get_past_time(self):
        delta_humanize = humanize.naturaltime(datetime.datetime.now() - self.last_updated_date)
        return change_suffix_time_to_thai(delta_humanize)
    
    def is_edited(self):
        if self.last_updated_date > self.created_date:
            return True
        return False
    

class Blog(me.Document):
    meta = {"collection": "blogs"}

    subject = me.StringField(required=True, max_length=255)
    body = me.StringField(required=True)
    owner = me.ReferenceField("User", dbref=True, required=True)
    created_date = me.DateTimeField(required=True)
    last_updated_date = me.DateTimeField(required=True)

    liked_by = me.ListField(me.ReferenceField("User", dbref=True))
    comments = me.ListField(me.ReferenceField("Comment", dbref=True))

    def get_body(self):
        return markdown.markdown(self.body)

    def get_natural_last_updated_date(self):
        return self.last_updated_date.strftime("%d %B %Y, %I:%M %p")
    
    def get_natural_created_date(self):
        return self.created_date.strftime("%d %B %Y, %I:%M %p")
    
    def get_past_time(self):
        delta_humanize = humanize.naturaltime(datetime.datetime.now() - self.last_updated_date)
        return change_suffix_time_to_thai(delta_humanize)
    
    def is_edited(self):
        if self.last_updated_date > self.created_date:
            return True
        return False