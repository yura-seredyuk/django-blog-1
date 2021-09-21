from django.contrib.admin import autodiscover
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200, null=False)
    text = models.TextField(null=False)
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(null=True)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.author.username + ' ' + self.title


