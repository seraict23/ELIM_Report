from django.urls import path
from . import views

app_name = "chapter2"
urlpatterns = [
    path("", views.Chapter2 , name="chapter2"),
    path("temporary/", views.Temp , name="temporary")
]
