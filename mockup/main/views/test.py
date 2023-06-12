from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from ..models import *

from .hwp import SecondThread, SecondThreadIntro, SecondThreadResultTable

import datetime


def Engineers(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    
    # 기술자 DB 저장
    Worker.objects.filter(worker=basic).delete()
    worker_length = int(req.POST['worker-length'])
    count = 1

    while count <= worker_length:
        Worker.objects.create(
            worker = basic,
            worker_role = req.POST['worker-'+str(count)+'-1'],
            worker_name = req.POST['worker-'+str(count)+'-2'],
            worker_class = req.POST['worker-'+str(count)+'-3'],
            worker_period = req.POST['worker-'+str(count)+'-4'],
            worker_job = req.POST['worker-'+str(count)+'-5'],
            worker_note = req.POST['worker-'+str(count)+'-6'],
        )
        count+=1

    
    # hwp 작성
    paramDictList = []

    worker = Worker.objects.filter(worker=basic)

    for i in worker:
        paramDict = {}
        for j in i._meta.get_fields():
            if j.name != "id" and j.name != "worker":
                paramDict[j.name] = getattr(i, j.name)
        paramDictList.append(paramDict)

    print(paramDictList)

    
    sub = SecondThread(paramDictList)
    sub.start()

    context = {
        "basic":basic
    }
    return render(req, 'main/file.html', context)



def Intro(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    
    # 지도 및 전경사진 db에 저장
    map = Map.objects.get(map=basic)

    # if 'map_titlePic' in req.POST :
    #     map.map_titlePic_name = req.POST['map_titlePic']
    #     map.map_titlePic_path = '/static/img/temp/'+ req.POST['map_titlePic']
    # if 'map_map' in req.POST:
    #     map.map_map_name = req.POST['map_map']
    #     map.map_map_path = '/static/img/temp/'+ req.POST['map_map']
    # map.save()
    
    # hwp 작성
    paramDict = {}
    paramDict['basic_name'] = basic.basic_name
    paramDict['basic_startAt'] = basic.basic_startAt
    paramDict['basic_endAt'] = basic.basic_endAt
    paramDict['basic_year'] = basic.basic_year
    paramDict['basic_month'] = basic.basic_month
    paramDict['basic_semi'] = basic.basic_semi

    paramDict['map_titlePic_name'] = map.map_titlePic_name
    paramDict['map_map_name'] = map.map_map_name

    print(paramDict)

    
    sub = SecondThreadIntro(paramDict)
    sub.start()

    context = {
        "basic":basic
    }
    return render(req, 'main/picture.html', context)


def ResultTable(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    contract = Contract.objects.get(contract=basic)
    facility = Facility.objects.get(facility = basic)
    worker = Worker.objects.filter(worker = basic)

    engineers = []
    for i in worker :
        engineers.append(i.worker_role)
        engineers.append(i.worker_name)
        engineers.append(i.worker_period)
        engineers.append(i.worker_class)
    print(engineers)


    paramDict = {
        "용역명": contract.contract_name,
        "점검기간": str(basic.basic_startAt).replace('-', '. ')+" ~ "+str(basic.basic_endAt).replace('-', '. '),
        "관리주체명": contract.contract_agency,
        "공동수급": contract.contract_joint,
        "계약방법": contract.contract_method,
        "종류": facility.facility_spec,
        "구분": facility.facility_category,
        "종별": facility.facility_class,
        "준공일": facility.facility_buildingDate,
        "금액": contract.contract_money,
        "등급": "양호",
        "주소": facility.facility_address,
        "규모": "연면적" + facility.facility_width_gross + " " + facility.facility_floor + " " + facility.facility_category,
        "시설물명": basic.basic_name,
        "startpoint":"",
        "engineers": engineers
    }

    print(paramDict)

    sub = SecondThreadResultTable(paramDict)
    sub.start()

    return HttpResponseRedirect(reverse("main:defect", args=(basic.id,)))