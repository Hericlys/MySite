from django.urls import path
from .import views

app_name = 'blog'

urlpatterns = [
    path('', views.posts, name='posts'),
    path('post_detail/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search_posts/', views.search_posts, name='search_posts'),
]
