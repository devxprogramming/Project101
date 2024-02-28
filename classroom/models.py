from django.db import models
from accounts.models import User
from uuid import uuid4



def avatar_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.course_code}.{ext}'
    return f'room_avatars/{filename}'


PRIVACY = (
    ('Public', 'Public'),
    ('Private', 'Private'),
)

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room_code = models.UUIDField(default=uuid4, editable=False, unique=True, null=True)
    course_code = models.CharField(max_length=255, null=True)
    course_title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    room_password = models.CharField(max_length=255, null=True, blank=True)
    room_privacy = models.CharField(max_length=255, null=True, choices=PRIVACY, blank=True)
    # slug = models.SlugField(unique=True)
    participants = models.ManyToManyField(User, related_name='participants')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    room_avatar = models.FileField(upload_to=avatar_directory_path, default='default.png', null=True, blank=True)

    def __str__(self):
        return self.course_title[:20]