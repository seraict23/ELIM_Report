
import sys
import os
from .forms import BuilidingForm, CommonForm, ContractForm, BuildingInfoForm, BuildingCategoryForm
from django.shortcuts import render

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from engine.common_gen import Worker
# Create your views here.

# 경로


def Common(req):
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

def Chapter1(req):
    return render(req, "common/playground.html")

def Chapter2(req):
    return render(req, "chapter02/chapter02.html")
