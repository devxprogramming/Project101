from django import forms
from django.forms import ModelForm
from classroom.models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host', 'participants']