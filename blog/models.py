from django.contrib.admin import autodiscover
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200, null=False)
    text = models.TextField(null=False)
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(null=True)
    # image = models.ImageField(upload_to='images')
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, height_field=100, width_field=100)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self) -> str:
        return self.author.username + ' ' + self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)