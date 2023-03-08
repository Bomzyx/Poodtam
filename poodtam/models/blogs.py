import mongoengine as me
import datetime
import markdown
import humanize

TAG_CHOICES = [
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


def change_suffix_time_to_thai(time):
    return (
        time.replace("ago", "ที่ผ่านมา")
        .replace("now", "ตอนนี้")
        .replace("seconds ", "วินาที")
        .replace("a minute ", "ไม่กี่นาที")
        .replace("minutes ", "นาที")
        .replace("an hour ", "1 ชั่วโมง")
        .replace("hours ", "ชั่วโมง")
        .replace("days ", "วัน")
        .replace("months ", "เดือน")
        .replace("years ", "ปี")
        .replace("year,", "ปี")
    )


class Comment(me.Document):
    meta = {"collection": "comments"}

    body = me.StringField(required=True)
    owner = me.ReferenceField("User", dbref=True, required=True)
    created_date = me.DateTimeField(required=True)
    last_updated_date = me.DateTimeField(required=True)

    liked_by = me.ListField(me.ReferenceField("User", dbref=True))
    comments = me.ListField(me.ReferenceField("Comment", dbref=True))

    def get_body(self):
        return markdown.markdown(self.body)

    def count_comment(self):
        count = 0
        for comment in self.comments:
            count += 1
            if comment.comments:
                count += comment.count_comment()

        return count

    def get_natural_last_updated_date(self):
        return self.last_updated_date.strftime("%d %B %Y, %I:%M %p")

    def get_natural_created_date(self):
        return self.created_date.strftime("%d %B %Y, %I:%M %p")

    def get_past_time(self):
        delta_humanize = humanize.naturaltime(
            datetime.datetime.now() - self.last_updated_date
        )
        return change_suffix_time_to_thai(delta_humanize)

    def is_edited(self):
        if self.last_updated_date > self.created_date:
            return True
        return False


class Blog(me.Document):
    meta = {"collection": "blogs"}

    subject = me.StringField(required=True, max_length=255)
    body = me.StringField()
    owner = me.ReferenceField("User", dbref=True, required=True)
    created_date = me.DateTimeField(required=True)
    last_updated_date = me.DateTimeField(required=True)

    tags = me.ListField(me.StringField(), choices=TAG_CHOICES)

    liked_by = me.ListField(me.ReferenceField("User", dbref=True))
    comments = me.ListField(me.ReferenceField("Comment", dbref=True))

    def get_body(self):
        return markdown.markdown(self.body)

    def count_comment(self):
        count = 0
        for comment in self.comments:
            count += 1
            if comment.comments:
                count += comment.count_comment()

        return count

    def get_natural_last_updated_date(self):
        return self.last_updated_date.strftime("%d %B %Y, %I:%M %p")

    def get_natural_created_date(self):
        return self.created_date.strftime("%d %B %Y, %I:%M %p")

    def get_past_time(self):
        delta_humanize = humanize.naturaltime(
            datetime.datetime.now() - self.last_updated_date
        )
        return change_suffix_time_to_thai(delta_humanize)

    def is_edited(self):
        if self.last_updated_date > self.created_date:
            return True
        return False
