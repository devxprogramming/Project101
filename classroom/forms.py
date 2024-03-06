from django.forms import ModelForm
from classroom.models import Room, Message, Resource


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host']
        
        
        
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        # exclude = ['user']
        
        
class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = "__all__"
        exclude = ['author']