from django.urls import path
from . import views

app_name = "common"
urlpatterns = [
    path("new/", views.CommonView, name="new"),
    path("submit/", views.Submit, name="submit"),
    path("", views.Cover, name="cover"),
    path("worker/", views.WorkerView , name="worker"),
    path("chapter3/", views.Chapter3 , name="chapter3")
]
