from django.db import models
from member.models import CustomUser

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    #related_name 역참조
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)