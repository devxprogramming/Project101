from django.urls import path
from dashboard import views


urlpatterns = [
    path('', views.home_page, name='dashboard'),
    path('dashboard/', views.home_page, name='dashboard'),
    path('search/', views.search_page, name='search'),
]
