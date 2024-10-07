from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('check_email/', views.check_email, name='check_email'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_done/<slug:token>/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]