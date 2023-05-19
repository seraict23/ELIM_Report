from django.urls import path
from . import views

app_name = "common"
urlpatterns = [
    path("", views.Cover, name="cover"),
    path("new/", views.CommonView, name="new"),
    path("submit/", views.Submit, name="submit"),
    path("picture/", views.Picture, name="picture"),
    path("worker/", views.WorkerView , name="worker"),
]
