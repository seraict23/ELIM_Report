from django.shortcuts import render

# Create your views here.
from chapter02.models import UsageChange
from common.models import Common

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from engine.chapter2 import Worker
# Create your views here.


def Chapter2(req):
    return render(req, "chapter02/chapter02.html")


def Temp(req):
    # currentBuilding = Common.objects.get(id=num)
    # for i in range(int(req.POST['usagechange-length'][0])):
    #     row="usagechange-"+str(i)
    #     usagechangecreation = UsageChange.objects.create(
    #         building=currentBuilding,
    #         existence=True,
    #         floor=req.POST[row][0],
    #         before_usefor=req.POST[row][1],
    #         before_area=req.POST[row][2],
    #         after_usefor=req.POST[row][3],
    #         after_area=req.POST[row][4],
    #         date = req.POST[row][5],
    #         note = req.POST[row][6],
    #     )
    row = int(req.POST['usagechange-length'][0])
    print(row)
    print(req.POST)
    tableitemlist=[]
    for i in range(row):
        tableitemlist.extend(req.POST.getlist('usagechange-'+str(i+1)))
    print(tableitemlist)

    return render(req, "chapter03/chapter03.html")

