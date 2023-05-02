from django.urls import path
from . import views

app_name = "engineer_db"
urlpatterns = [
    path("", views.info, name="info"),
    path("<int:years>", views.yearCalculator, name="yearFilter")
]
