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


    # listOfHeads = ['usagechange-length', 'structurechange-length', 'environmentchange', 'expansion-length', 'overload', 'accident']


    paramDict = {}

    # 용도변경
    row = int(req.POST['usagechange-length'])
    tableitemlist=[]
    for i in range(row):
        tableitemlist.extend(req.POST.getlist('usagechange-'+str(i+1)))
    print(tableitemlist)

    paramDict['usagechange-row'] = row
    paramDict['usagechange-list'] = tableitemlist



    # 구조변경
    row = int(req.POST['structurechange-length'])
    tableitemlist=[]
    for i in range(row):
        tableitemlist.extend(req.POST.getlist('structurechange-'+str(i+1)))
    print(tableitemlist)

    paramDict['structurechange-row'] = row
    paramDict['structurechange-list'] = tableitemlist


    # 주변조건
    row = int(req.POST['environmentchange'])
    tableitemlist=[]
    for i in range(row):
        tableitemlist.extend(req.POST.getlist('environmentchange-'+str(i+1)))
    print(tableitemlist)

    paramDict['environmentchange-row'] = row
    paramDict['environmentchange-list'] = tableitemlist


    print(paramDict)




    # 이미지 처리 list > table 이 아니라 그냥 하나씩?
    print(req.POST)
    if '1-usagechange-pic1' in req.POST:
        paramDict['pic-1']=[]
        paramDict['pic-1'].append(req.POST['1-usagechange-pic1'])
        paramDict['pic-1'].append(req.POST['1-usagechange-pic2'] if '1-usagechange-pic2' in req.POST else 'default.jpg')
    else :
        print("NOT 1-usagechange-pic1 in req.POST")

    if '2-structurechange-pic1' in req.POST:
        paramDict['pic-2']=[]
        paramDict['pic-2'].append(req.POST['2-structurechange-pic1'])
        paramDict['pic-2'].append(req.POST['2-structurechange-pic2'] if '2-structurechange-pic2' in req.POST else 'default.jpg')
    else : 
        print("NOT 2-structurechange-pic1 in req.POST")

    if '3-environmentchange-pic1' in req.POST:
        paramDict['pic-3']=[]
        paramDict['pic-3'].append(req.POST['3-environmentchange-pic1'])
        paramDict['pic-3'].append(req.POST['3-environmentchange-pic2'] if '3-environmentchange-pic2' in req.POST else 'default.jpg')
    else : 
        print("NOT 3-environmentchange-pic1 in req.POST")


    # sub = Worker(paramDict)
    # sub.start()


    return render(req, "chapter03/chapter03.html")

