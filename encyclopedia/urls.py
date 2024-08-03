from django.urls import path
from django.urls import include, path

from . import views


urlpatterns = [
    path("", views.index, name="index"), 
    path("search", views.search, name="search"), 
    path("newpage", views.create, name="create"), 
    path("edit/<str:name>", views.edit, name="edit"), 
    path("<str:name>", views.get, name="get"), 
    
    
]
