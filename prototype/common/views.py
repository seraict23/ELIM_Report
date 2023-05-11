
import sys
import os
from .forms import BuilidingForm, CommonForm, ContractForm, BuildingInfoForm, BuildingCategoryForm
from django.shortcuts import render

from .models import Common, Worker
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from engine.test import Worker as Ace
# Create your views here.


def CommonView(req):
    common_form = CommonForm()
    building_form = BuilidingForm()
    contract_form = ContractForm()
    building_info_form = BuildingInfoForm()
    building_category_form = BuildingCategoryForm()

    return render(
        req,
        'common/common.html',
        {
            'commonform': common_form,
            'buildingform': building_form,
            "contractform": contract_form,
            "buildinginfoform": building_info_form,
            "buildingcategoryform": building_category_form
        })


def Cover(req):
    return render(req, "prototype/cover.html")




def Submit(req):
    # sub = Worker(req.POST)
    # sub.start()

    print(req.POST)
    return render(req, "common/playground.html")


def WorkerView(req):

    if req.method == 'POST':
        print(req.POST)
        row = int(req.POST['worker-length'])
        building = Common.objects.get(building_name="국민은행여의도본점")

        for i in range(row):
            Worker.objects.create(
                job=building,
                worker_name=req.POST.getlist('worker-'+str(i+1))[0],
                worker_role=req.POST.getlist('worker-'+str(i+1))[1],
                worker_class=req.POST.getlist('worker-'+str(i+1))[2],
                worker_startDate=req.POST.getlist('worker-'+str(i+1))[3],
            )
        
        tableitemlist=[]
        for i in range(row):
            tableitemlist.extend(req.POST.getlist('worker-'+str(i+1)))
        print(tableitemlist)
        sub = Ace(tableitemlist, row)
        sub.start()

        return render(req, "common/playground.html")
        
    else:
        building = Common.objects.get(building_name="국민은행여의도본점")
        report_date = str(building.report_date)
        context = {'report_date': report_date}
        return render(req, "common/worker.html", context)



def Chapter3(req):
    return render(req, "chapter03/chapter03.html")
