from django.db import models
from accounts.models import User
from uuid import uuid4

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room_code = models.UUIDField(default=uuid4, editable=False, unique=True, null=True)
    course_code = models.CharField(max_length=255, null=True)
    course_title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    # slug = models.SlugField(unique=True)
    participants = models.ManyToManyField(User, related_name='participants')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)