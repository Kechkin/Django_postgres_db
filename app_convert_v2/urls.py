from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add_data/', views.add_data, name='add_data'),
    path('search/', views.search, name='search'),
    path('convert_result/', views.converter_to, name='converter_to'),
]


