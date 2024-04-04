from django.urls import path
from classroom import views

urlpatterns = [
    path('create-room/', views.create_room, name='create_room'),
    path('update-room/<str:pk>/', views.update_room, name='update_room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete_room'),
    path('all-rooms/', views.show_all_rooms, name='all_rooms'),
    path('private-room/<str:pk>/', views.private_room, name='private_room'),
    path('room-message/<str:pk>/', views.room_message, name='room_message'),
    path('delete-message/<str:pk>', views.delete_message, name="delete_message"),
    path('delete-all-rooms/', views.delete_all_rooms, name="delete_all_rooms"),
    path('create-resources/', views.create_resources, name='create_resources'),
    path('download/<str:pk>/', views.download_reference_material, name='download_reference_material'),
]
