from django.urls import path
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('search_project/', views.search_projects, name='search_projects'),
]