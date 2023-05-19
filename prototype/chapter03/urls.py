from django.urls import path
from . import views

app_name = "chapter3"
urlpatterns = [
    path("", views.Chapter3 , name="chapter3"),
    path("exceldata/", views.ExcelData , name="exceldata"),
    path("cleardata/", views.ClearData , name="cleardata"),
    path("viewdata/", views.ViewData , name="viewdata"),
    path("drawing/", views.Drawing, name="drawing")
]
