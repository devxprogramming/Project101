from django.contrib import admin
from accounts.models import User, Profile, Department

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Department)