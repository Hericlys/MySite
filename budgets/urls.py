from django.urls import path
from . import views


app_name = "budgets"

urlpatterns = [
    path('create/',views.create_budget, name="create"),
]
