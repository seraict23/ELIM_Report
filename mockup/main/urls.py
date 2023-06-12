from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("new/", views.New, name="new"),
    path("load/", views.Load, name="load"),
    path("<int:basic_id>/file/", views.File, name="file"),
    path("<int:basic_id>/facility/", views.FacilView, name="facility"),
    path("<int:basic_id>/picture/", views.Picture, name="picture"),
    
    path("<int:basic_id>/defect/", views.DefectView, name="defect"),


    path("<int:basic_id>/uploadBML/", views.PDFConverter, name="uploadBML"),
    path("<int:basic_id>/uploadFML/", views.FMLTest, name="uploadFML"),
    path("<int:basic_id>/uploadEXCEL/", views.ExcelData, name="uploadEXCEL"),
    path("<int:basic_id>/uploadDWG/", views.DWGTest, name="uploadDWG"),
    path("<int:basic_id>/<str:fileType>/fileReady/", views.FileReady, name="FileReady" ),

    path("<int:basic_id>/public/", views.PubView, name="public"),


    path("<int:basic_id>/test/", views.Engineers, name="test"),
    path("<int:basic_id>/test2/", views.Intro, name="test2"),
    path("<int:basic_id>/test3/", views.ResultTable, name="test3")
]
