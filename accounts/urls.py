from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    
    path('user-profile/<str:pk>', views.user_profile, name="user_profile"),
    path('change-password', views.change_password, name="change_password"),
]