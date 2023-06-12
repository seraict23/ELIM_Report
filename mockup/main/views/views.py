from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from ..models import *

import os, glob
from pathlib import Path
from pypdf import PdfReader, PdfWriter

import win32com.client as win32
from threading import Thread



def New(req):

    # 입력받은 값 > 기초정보
    basic_name = req.POST['basic_name']
    basic_startAt = req.POST['basic_startAt']
    basic_endAt = req.POST['basic_endAt']

    # 종속변수(년도, 월, 반기) 처리
    basic_year = str(basic_startAt).split('-')[0]
    basic_month = str(basic_startAt).split('-')[1]
    if int(basic_month) > 6:
        basic_semi = "하반기"
    else : 
        basic_semi = "상반기"

    # 데이터 테이블 생성 및 기초정보 입력
    basic = Basic.objects.create(
        basic_name=basic_name,
        basic_startAt=basic_startAt,
        basic_endAt=basic_endAt,
        basic_year = basic_year,
        basic_month = basic_month,
        basic_semi = basic_semi
    )

    # 계약정보
    contract_name = basic_name + ' ' + basic_year + ' ' + basic_semi + ' 정기안전점검'

    # 데이터 초기화
    Contract.objects.create(
        contract=basic,
        contract_name=contract_name,
    )
    Facility.objects.create(
        facility=basic,
        facility_name = basic_name,
        facility_spec="-",
    )
    Map.objects.create(
        map=basic,
        map_titlePic_name = "-",
        map_titlePic_path = "-",
        map_map_name = "-",
        map_map_path = "-",
    )
    UploadFile.objects.create(
        file=basic,
        file_name_BML = "",
        file_name_FML = "",
        file_name_EXCEL = "",
        file_name_DWG = "",
    )
    print(basic.id)
    redirect_url = reverse("main:file", args=(basic.id,))
    return JsonResponse({"redirect_url": redirect_url})


def Load(req):
    if req.method == 'POST':
        pk = req.POST['pk']
        try:
            basic = Contract.objects.get(pk=pk)
            print(basic.id)
        except Contract.DoesNotExist:
            print("???")

        redirect_url = reverse("main:file", args=(basic.id,))
        return JsonResponse({"redirect_url": redirect_url})

    else : 
        contract = Contract.objects.order_by("-id")
        context = {
            'contract': contract,
        }
        return render(req, 'main/load.html', context)


def File(req, basic_id):
    if req.method == 'POST':
        # POST 값 가져오기
        basic_id = req.POST['basic_id']
        basic_name = req.POST['basic_name']
        basic_startAt = req.POST['basic_startAt']
        basic_endAt = req.POST['basic_endAt']

        # basic 모델
        basic = Basic.objects.get(pk=basic_id)
        basic.basic_name = basic_name
        basic.basic_startAt = basic_startAt
        basic.basic_endAt = basic_endAt


        # 종속변수(년도, 월, 반기) 처리
        basic.basic_year = str(basic_startAt).split('-')[0]
        basic.basic_month = str(basic_startAt).split('-')[1]
        if int(basic.basic_month) > 6:
            basic.basic_semi = "하반기"
        else : 
            basic.basic_semi = "상반기"
        basic.save()

        # 기술자
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

        # 파일
        # uploadfile = UploadFile.objects.get(file=basic)
        # if 'file_name_BML' in req.POST:
        #     uploadfile.file_name_BML = req.POST['file_name_BML']
        # if 'file_name_FML' in req.POST:
        #     uploadfile.file_name_FML = req.POST['file_name_FML']
        # if 'file_name_EXCEL' in req.POST:
        #   uploadfile.file_name_EXCEL = req.POST['file_name_EXCEL']
        # if 'file_name_DWG' in req.POST:
        #     uploadfile.file_name_DWG = req.POST['file_name_DWG']
        # uploadfile.save()

        # 계약정보
        contract = Contract.objects.get(contract=basic)
        contract.contract_name = req.POST['contract_name']
        contract.contract_joint = req.POST['contract_joint']
        contract.contract_method = req.POST['contract_method']
        contract.contract_agency = req.POST['contract_agency']
        contract.contract_money = req.POST['contract_money']
    
        contract.save()

        redirect_url = reverse("main:picture", args=(basic_id,))
        return JsonResponse({"redirect_url": redirect_url})
        
    else:
        basic = Basic.objects.get(pk=basic_id)
        contract = Contract.objects.get(contract=basic)
        worker = Worker.objects.filter(worker=basic).order_by("id")
        context = {
            'basic' : basic,
            'contract': contract,
            'worker' : worker,
        }
        return render(req, 'main/file.html', context)


def FacilView(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    facility = Facility.objects.get(facility=basic)
    FMS = FacilityManagementStatus.objects.get_or_create(facilityManagementStatus=basic)

    if req.method=='POST': 

        # 이하를 다음으로 대체 가능
        # for i in list(req.POST.keys()):
        #     if i =='facility_constructStartAt' or 'facility_constructEndAt' or 'facility_buildingDate':
        #         pass
        #     else:
        #         facility[i] = req.POST[i]

        print(req.POST)
        facility.facility_address = req.POST['facility_address']
        facility.facility_width_land = req.POST['facility_width_land']
        facility.facility_width_building = req.POST['facility_width_building']
        facility.facility_width_gross = req.POST['facility_width_gross']
        facility.facility_structure = req.POST['facility_structure']
        facility.facility_floor = req.POST['facility_floor']

        facility.facility_spec = req.POST['facility_spec']
        facility.facility_class = req.POST['facility_class']
        facility.facility_category = req.POST['facility_category']
        facility.facility_usage = req.POST['facility_usage']

        facility.facility_architect = req.POST['facility_architect']
        facility.facility_supervisor = req.POST['facility_supervisor']
        facility.facility_builder = req.POST['facility_builder']
        if req.POST['facility_constructStartAt'] != '':
            facility.facility_constructStartAt = req.POST['facility_constructStartAt']
        if req.POST['facility_constructEndAt'] != '':
            facility.facility_constructEndAt = req.POST['facility_constructEndAt']
        if req.POST['facility_buildingDate'] != '':
            facility.facility_buildingDate = req.POST['facility_buildingDate']
        facility.facility_old = req.POST['facility_old']
        
        facility.save()


        # 용도변경
        # 초기화
        if len(FMS_Usage.objects.filter(basic=basic))>0:    
            FMS_Usage.objects.filter(basic=basic).delete()  
        
        # 목록에 삽입
        facility_usage_row = int(req.POST['FMS_usage'])
        FMS[0].FMS_Usage = facility_usage_row

        # 각 항목 작성
        for i in range(1, facility_usage_row+1):
            FMS_Usage.objects.create(
                basic=basic,
                floor = req.POST['1-'+str(i)+'-1'],
                before_useFor = req.POST['1-'+str(i)+'-2'],
                before_area = req.POST['1-'+str(i)+'-3'],
                after_useFor = req.POST['1-'+str(i)+'-4'],
                after_area = req.POST['1-'+str(i)+'-5'],
                date = req.POST['1-'+str(i)+'-6'],
                note = req.POST['1-'+str(i)+'-7'],
            )

        # 구조변경
        # 초기화
        if len(FMS_Structure.objects.filter(basic=basic))>0:    
            FMS_Structure.objects.filter(basic=basic).delete()  
        
        # 목록에 삽입
        facility_structure_row = int(req.POST['FMS_structure'])
        FMS[0].FMS_Structure = facility_structure_row

        # 각 항목 작성
        for i in range(1, facility_structure_row+1):
            FMS_Structure.objects.create(
                basic=basic,
                wing = req.POST['2-'+str(i)+'-1'],
                material = req.POST['2-'+str(i)+'-2'],
                mark = req.POST['2-'+str(i)+'-3'],
                location = req.POST['2-'+str(i)+'-4'],
                content = req.POST['2-'+str(i)+'-5'],
                personInCharge = req.POST['2-'+str(i)+'-6'],
                date = req.POST['2-'+str(i)+'-7'],
            )

        
        # 환경변화
        # 초기화
        if len(FMS_Env.objects.filter(basic=basic))>0:    
            FMS_Env.objects.filter(basic=basic).delete() 

        # 목록에 삽입
        facility_env_row = int(req.POST['FMS_env'])
        FMS[0].FMS_Env = facility_env_row

        # 각 항목 작성
        if facility_env_row > 0:
            for i in range(1, 4):
                FMS_Env.objects.create(
                    basic=basic,
                    location = req.POST['3-'+str(i)+'-1'] if '3-'+str(i)+'-1' in req.POST else '-',
                    before = req.POST['3-'+str(i)+'-2'] if '3-'+str(i)+'-2' in req.POST else '-',
                    after = req.POST['3-'+str(i)+'-3'] if '3-'+str(i)+'-3' in req.POST else '-',
                )

        # 증개축
        # 초기화
        if len(FMS_Expansion.objects.filter(basic=basic))>0:    
            FMS_Expansion.objects.filter(basic=basic).delete()  
        
        # 목록에 삽입
        facility_expansion_row = int(req.POST['FMS_expansion'])
        FMS[0].FMS_Expansion= facility_expansion_row

        # 각 항목 작성
        for i in range(1, facility_expansion_row+1):
            FMS_Expansion.objects.create(
                basic=basic,
                floor = req.POST['4-'+str(i)+'-1'],
                before_useFor = req.POST['4-'+str(i)+'-2'],
                before_area = req.POST['4-'+str(i)+'-3'],
                after_useFor = req.POST['4-'+str(i)+'-4'],
                after_area = req.POST['4-'+str(i)+'-5'],
                date = req.POST['4-'+str(i)+'-6'],
                note = req.POST['4-'+str(i)+'-7'],
            )
        
        
        # 과하중
        # 초기화
        if len(FMS_Overload.objects.filter(basic=basic))>0:    
            FMS_Overload.objects.filter(basic=basic).delete()  
        
        # 목록에 삽입
        facility_overload_row = int(req.POST['FMS_overload'])
        FMS[0].FMS_Overload = facility_overload_row

        # 각 항목 작성
        for i in range(1, facility_overload_row+1):
            FMS_Overload.objects.create(
                basic=basic,
                type = req.POST['5-'+str(i)+'-1'],
                location = req.POST['5-'+str(i)+'-2'],
                text = req.POST['5-'+str(i)+'-3'],
                note = req.POST['5-'+str(i)+'-4'],
            )


        # 사고
        # 초기화
        if len(FMS_Accident.objects.filter(basic=basic))>0:    
            FMS_Accident.objects.filter(basic=basic).delete()  
        
        # 목록에 삽입
        facility_accident_row = int(req.POST['FMS_accident'])
        FMS[0].FMS_Accident = facility_accident_row

        # 각 항목 작성
        for i in range(1, facility_accident_row+1):
            FMS_Accident.objects.create(
                basic=basic,
                title = req.POST['6-'+str(i)+'-1'],
                content = req.POST['6-'+str(i)+'-2'],
                location = req.POST['6-'+str(i)+'-3'],
                degree_of_damage = req.POST['6-'+str(i)+'-4'],
                action = req.POST['6-'+str(i)+'-5'],
                status = req.POST['6-'+str(i)+'-6'],
            )

        FMS[0].save()

        redirect_url = reverse("main:defect", args=(basic_id,))
        return JsonResponse({"redirect_url": redirect_url})

    else : 
        FMS_usage = FMS_Usage.objects.filter(basic=basic)
        FMS_structure = FMS_Structure.objects.filter(basic=basic)
        FMS_env = FMS_Env.objects.filter(basic=basic)
        FMS_expansion = FMS_Expansion.objects.filter(basic=basic)
        FMS_overload = FMS_Overload.objects.filter(basic=basic)
        FMS_accident = FMS_Accident.objects.filter(basic=basic)

        FMS = FacilityManagementStatus.objects.filter(facilityManagementStatus=basic)[0]

        context = {
            'basic': basic,
            'facility': facility,
            'FMS_usage': FMS_usage,
            'FMS_structure': FMS_structure,
            'FMS_env': FMS_env,
            'FMS_expansion': FMS_expansion,
            'FMS_overload': FMS_overload,
            'FMS_accident': FMS_accident,
            'FMS': FMS
        }
        return render(req, 'main/facility.html', context)


def Picture(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    map = Map.objects.get(map = basic)
    if req.method == 'POST':
        print(req.POST)

        # 부위별 사진
        PartPhoto.objects.filter(partPhoto = basic).delete()

        partPhoto_length = int(req.POST['piccount'])
        count = 1

        while count <= partPhoto_length:
            PartPhoto.objects.create(
                partPhoto = basic,
                partPhoto_number = int(count),
                partPhoto_name = req.POST['picture-'+str(count)],
                partPhoto_note = req.POST['picture-note-'+str(count)],
                partPhoto_path = '/static/img/temp/'+ req.POST['picture-'+str(count)],
            )
            count+=1

        # 전경사진
        if 'map_titlePic' in req.POST :
            map.map_titlePic_name = req.POST['map_titlePic']
            map.map_titlePic_path = '/static/img/temp/'+ req.POST['map_titlePic']
        if 'map_map' in req.POST:
            map.map_map_name = req.POST['map_map']
            map.map_map_path = '/static/img/temp/'+ req.POST['map_map']
        map.save()

        redirect_url = reverse("main:facility", args=(basic_id,))
        return JsonResponse({"redirect_url": redirect_url})
    

    else :
        partPhoto = PartPhoto.objects.filter(partPhoto=basic).order_by("partPhoto_number")
        context = {
                'basic': basic,
                'map': map,
                'partPhoto': partPhoto
            }
        return render(req, 'main/picture.html', context)
    

def DefectView(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    defect = Defect.objects.filter(defect=basic_id).order_by('id')
    context = {
        "basic":basic,
        "defect":defect
    }
    return render(req, 'defect/defect.html', context)


def PubView(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    if req.method == "POST":
        public=Public.objects.get(public=basic)
        print(req.POST)

        for i in list(req.POST.keys()):
            public[i] = req.POST[i]

        context={
            'basic': basic,
            'public': public,
        }   
        return render( req, 'main/public.html', context)
    
    else:
        public = Public.objects.get_or_create(public=basic)[0]
        context={
            'basic': basic,
            'public':public
        }
        return render( req, 'main/public.html', context)
    


