from django.urls import path
from . import views

urlpatterns = [
    path('', views.signupview, name='signup'),
    path('login/' ,views.login, name='login'),
    path('home/', views.home, name='home'),
    path('get_bot_response/', views.get_bot_response, name='get_bot_response'),
]

