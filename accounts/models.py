from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.db.models.signals import post_save

def avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.user.id}.{ext}'
    return f'avatars/{filename}'

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

LEVEL = (
    ('100', '100'),
    ('200', '200'),
    ('300', '300'),
    ('4000', '400'),
)

class User(AbstractUser):
    school_id = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    gender = models.CharField(max_length=200, choices=GENDER)


class Profile(models.Model):
    pid = models.URLField(default=uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, choices=GENDER)
    level = models.CharField(max_length=200, choices=LEVEL)
    password = models.CharField(max_length=255, null=True)
    avatar = models.FileField(upload_to=avatar_path, default='default.jpg', null=True, blank=True)

    


def create_profile(sender, created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)