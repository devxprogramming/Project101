from django.urls import path
from classroom import views

urlpatterns = [
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<str:pk>/', views.update_room, name='update_room'),
    # path('delete-room/<str:pk>/', views.delete_room, name='delete_room'),
]
