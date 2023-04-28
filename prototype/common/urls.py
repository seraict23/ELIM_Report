from django.urls import path
from . import views

app_name = "common"
urlpatterns = [
    path("", views.Test, name="test"),
    path("new/", views.Common, name="new"),
    path("submit/", views.Submit, name="submit")
]
