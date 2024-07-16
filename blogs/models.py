from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    text_content = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title
