from django.shortcuts import render

# Create your views here.
from .models import Engineer

from datetime import date, timedelta


def info(req):
    q = req.GET.get('year')

    if q is None:
        context = {"required_year":0}
        return render(req, "engineer_db/info.html", context)
    
    else:
        today = date.today()
        today.replace(year=(int(today.year)-int(req.GET.get('year'))))
        
        required_year = today.replace(year=(int(today.year)-int(req.GET.get('year'))))
        print(required_year)

        old_engineer = Engineer.objects.filter(start_workAt__lte = required_year)

        engineer_list = old_engineer
        context = {
            "engineer_list":engineer_list,
            "required_year": req.GET.get('year')
        }
        return render(req, "engineer_db/info.html", context)
    
    

def yearCalculator(req, years):
    today = date.today()
    today.replace(year=(int(today.year)-int(years)))
    
    required_year = today.replace(today.year-int(req.GET.get('year')))

    old_engineer = Engineer.objects.filter(start_workAt__lte = required_year)

    engineer_list = old_engineer
    context = {
        "engineer_list":engineer_list,
        "required_year": req.GET.get('year')
    }

    return render(req, "engineer_db/info.html", context)