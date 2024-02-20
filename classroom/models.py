from django.db import models
from accounts.models import User

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course_code = models.CharField(max_length=255, null=True)
    course_title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    slug = models.SlugField(unique=True)
    participants = models.ManyToManyField(User, related_name='participants')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)