from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name="login"),
    path('index/', views.index, name='index'),
    path('index/add_data/', views.add_data, name='add_data'),
    path('index/search/', views.search, name='search'),
    path('index/convert_result/', views.converter_to, name='converter_to'),
]


