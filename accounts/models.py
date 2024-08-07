from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.db.models.signals import post_save

def avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.school_id}.{ext}'
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

ACCOUNT_TYPE = (
    ("Student", "Student"),
    ("Lecturer","Lecturer")
)



class User(AbstractUser):
    school_id = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=200, choices=GENDER)
    account_type = models.CharField(max_length=255, choices=ACCOUNT_TYPE, null=True)
    
    USERNAME_FIELD = 'school_id'
    REQUIRED_FIELDS = ['username']


class Profile(models.Model):
    pid = models.URLField(default=uuid4, unique=True, editable=False)
    account_type = models.CharField(max_length=255,choices=ACCOUNT_TYPE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, choices=GENDER)
    level = models.CharField(max_length=200, choices=LEVEL)
    password = models.CharField(max_length=255, null=True)
    avatar = models.FileField(upload_to=avatar_path, default='default.png', null=True, blank=True)
    
    def __str__(self):
        return self.user.school_id
    
    
class Department(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

    


def create_profile(sender, created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            school_id=instance.school_id,
            full_name=instance.full_name,
            gender=instance.gender,
            account_type=instance.account_type
                               )

def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)