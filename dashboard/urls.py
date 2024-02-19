from django.urls import path
from dashboard import views


urlpatterns = [
    path('dashboard/', views.home_page, name='dashboard')
]
