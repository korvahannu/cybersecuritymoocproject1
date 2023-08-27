from django.urls import path
from . import views

app_name = "brokensite"
urlpatterns = [
    path('', views.index, name="index"),
    path('delete/', views.delete, name="delete"),
    path('search/', views.search, name="search"),
]
