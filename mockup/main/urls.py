from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("new/", views.New, name="new"),
    path("load/", views.Load, name="load"),
    path("<int:basic_id>/file/", views.File, name="file"),
    path("<int:basic_id>/fileload/", views.PDFConverter, name="fileload"),
    path("<int:basic_id>/isfileready/", views.IsFileReady, name="isfileready"),
    path("<int:basic_id>/common/", views.Common, name="common"),
    path("<int:basic_id>/picture/", views.Picture, name="picture"),
]
