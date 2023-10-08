from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather),  #the path for our index view
]