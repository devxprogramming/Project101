from django.db import models
from accounts.models import User, Department, Profile
from uuid import uuid4



def avatar_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.course_code}.{ext}'
    return f'room_avatars/{filename}'

def resources_file_path(instance, filename):
    file_ext = filename.split(".")[-1]
    filename = f"{instance.filename}.{file_ext}"
    return f"resources/{filename}"

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
    resources = models.ManyToManyField('Resource', related_name='resources', null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    room_avatar = models.FileField(upload_to=avatar_directory_path, default='default.png', null=True, blank=True)

    def __str__(self):
        return self.course_title[:10]
    
    def check_password(self, password):
        if self.room_password is None:
            # Set room_privacy to Public
            self.room_privacy = 'Public'
            self.save()
        elif self.room_password is not None:
            self.room_privacy = 'Private'
            self.save()
            


class Message(models.Model):
    message_code = models.UUIDField(default=uuid4, unique=True, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:10]
    


class Resource(models.Model):
    file_code = models.UUIDField(default=uuid4, unique=True, editable=False)
    filename = models.CharField(max_length=999999, unique=True)
    upload = models.FileField(upload_to=resources_file_path, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.filename}"