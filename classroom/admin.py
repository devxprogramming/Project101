from django.contrib import admin
from classroom.models import Room, Message, Resource, StudyAi


class RoomAdmin(admin.ModelAdmin):
    list_display = ['course_title', 'course_code', 'room_password', 'description', 'host', 'room_code']
    readonly_fields = ['host', 'room_code']



admin.site.register(Room, RoomAdmin)
admin.site.register(Message)
admin.site.register(Resource)
admin.site.register(StudyAi)