from django.urls import path
from . import views

app_name = "brokensite"
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:note_id>/', views.delete, name="delete")
]
