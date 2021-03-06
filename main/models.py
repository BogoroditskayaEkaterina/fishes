from django.db.models import *
from django.contrib.auth.models import User

class Blog(Model):
    title = CharField(max_length=80)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    author = ForeignKey(User, on_delete=CASCADE, default=1)

    def __str__(self):
        return str(self.title)


class Post(Model):
    blog = ForeignKey(Blog, on_delete=CASCADE)
    subject = CharField(max_length=80)
    text = TextField(max_length=4096)
    created_at = DateTimeField('creation timestamp', auto_now_add=True)
    updated_at = DateTimeField('update timestamp', auto_now=True)
    image = ImageField(upload_to='media/img', null=True, blank=True)

    def __str__(self):
        return str(self.subject)



