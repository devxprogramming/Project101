from django.urls import path
from classroom import views

urlpatterns = [
    path('create-room/', views.create_room, name='create_room'),
]
