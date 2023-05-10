from django.urls import path
from . import views

app_name = "common"
urlpatterns = [
    path("new/", views.CommonView, name="new"),
    path("submit/", views.Submit, name="submit"),
    path("", views.Cover, name="cover"),
    path("chapter1/", views.Chapter1 , name="chapter1"),
    path("chapter3/", views.Chapter3 , name="chapter3")
]
