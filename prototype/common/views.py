
import sys
import os
from .forms import BuilidingForm, CommonForm, ContractForm, BuildingInfoForm, BuildingCategoryForm
from django.shortcuts import render
from .models import Common

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from engine.common_gen import Worker
# Create your views here.

# 경로


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

    Common.objects.create(
        building_name=req.POST['building_name'],
        report_date=req.POST['report_date'],
        building_date=req.POST['building_date'],
        building_address=req.POST['building_address'],
        building_category=req.POST['building_category'],
        contract_joint=req.POST['contract_joint'],
        contract_method=req.POST['contract_method'],
        contract_money=req.POST['contract_money'],
        building_pic=req.POST['building_image'],
        building_map=req.POST['map_image'],
    )

    return render(req, "common/playground.html")

def Chapter1(req):
    return render(req, "chapter01/chapter01.html")

def Chapter2(req):
    return render(req, "chapter02/chapter02.html")

def Chapter3(req):
    return render(req, "chapter03/chapter03.html")
