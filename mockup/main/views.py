from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import Basic, Contract, Facility, Worker, UploadFile, Map

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
        contract_name = req.POST['contract_name']
        try:
            basic = Contract.objects.get(contract_name=contract_name)
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
        uploadfile = UploadFile.objects.get(file=basic)
        if 'file_name_BML' in req.POST:
            uploadfile.file_name_BML = req.POST['file_name_BML']
        if 'file_name_FML' in req.POST:
            uploadfile.file_name_FML = req.POST['file_name_FML']
        if 'file_name_EXCEL' in req.POST:
          uploadfile.file_name_EXCEL = req.POST['file_name_EXCEL']
        if 'file_name_DWG' in req.POST:
            uploadfile.file_name_DWG = req.POST['file_name_DWG']
        uploadfile.save()



        # 전경사진
        map = Map.objects.get(map=basic)
        if 'map_titlePic' in req.POST :
            map.map_titlePic_name = req.POST['map_titlePic']
            map.map_titlePic_path = '/static/img/temp/'+ req.POST['map_titlePic']
        if 'map_map' in req.POST:
            map.map_map_name = req.POST['map_map']
            map.map_map_path = '/static/img/temp/'+ req.POST['map_map']
        map.save()


        # 계약정보
        contract = Contract.objects.get(contract=basic)
        contract_name = basic.basic_name + ' ' + basic.basic_year + ' ' + basic.basic_semi + ' 정기안전점검'
        contract.contract_name=contract_name
        contract.save()


        redirect_url = reverse("main:common", args=(basic_id,))
        return JsonResponse({"redirect_url": redirect_url})
        
    else:
        basic = Basic.objects.get(pk=basic_id)
        contract = Contract.objects.get(contract=basic)
        map = Map.objects.get(map = basic)
        worker = Worker.objects.filter(worker=basic).order_by("id")
        context = {
            'basic' : basic,
            'contract': contract,
            'map' : map,
            'worker' : worker,
        }
        return render(req, 'main/file.html', context)


def PDFConverter(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)

    print("gogo")

    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = str(BASE_DIR)+"/static/"
    pdf_folder = os.path.join(PATH, "시설물대장")
    cropped_pdf_folder = os.path.join(PATH,"tmp")

    for pdf in glob.glob(pdf_folder+"\\*.pdf"):
        reader = PdfReader(pdf)
        for num_page, page in enumerate(reader.pages, start=1):        
            if num_page == 2:
                writer = PdfWriter()
                writer.add_page(page)
                with open(cropped_pdf_folder + "\\" + pdf.split('\\')[-1].replace(".pdf","") + "_기본현황.pdf", "wb") as fp:
                    writer.write(fp)
            elif num_page == 3:
                writer = PdfWriter()
                writer.add_page(page)
                with open(cropped_pdf_folder + "\\" + pdf.split('\\')[-1].replace(".pdf","") + "_상세제원.pdf", "wb") as fp:
                    writer.write(fp)

    # 워드 처리

    class WordApp:
        def __init__(self):
            try:
                self.word = win32.gencache.EnsureDispatch('Word.Application')

                for cropped_pdf in glob.glob(cropped_pdf_folder+"\\*.pdf"):
                    self.word.Documents.Open(cropped_pdf)
                    try :
                        doc=self.word.ActiveDocument

                        basic = Basic.objects.get(pk=basic_id)

                        facility = Facility.objects.get(facility=basic)
                        

                        if cropped_pdf.endswith("_기본현황.pdf"):
                            tables = doc.Tables
                            table = tables(1)

                            시설물번호 = table.Cell(Row=3, Column=1).Range.Text.replace('\r\x07','').replace('\r','')
                            시설물명 = table.Cell(Row=3, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
                            시설물종류 = table.Cell(Row=3, Column=6).Range.Text.replace('\r\x07','').replace('\r','')
                            시설물종별 = table.Cell(Row=3, Column=7).Range.Text.replace('\r\x07','').replace('\r','')
                            시설물구분 = table.Cell(Row=3, Column=8).Range.Text.replace('\r\x07','').replace('\r','')

                            first_addr = table.Cell(Row=5, Column=1).Range.Text.replace('\r\x07','').replace('\r','')
                            second_addr = table.Cell(Row=5, Column=2).Range.Text.replace('\r\x07','').replace('\r','')
                            third_addr = table.Cell(Row=5, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
                            fourth_addr = table.Cell(Row=5, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
                            시설물주소 = " ".join([first_addr, second_addr, third_addr, fourth_addr])

                            관리주체 = table.Cell(Row=5, Column=5).Range.Text.replace('\r\x07','').replace('\r','')
                            준공일 = table.Cell(Row=9, Column=2).Range.Text.replace('\r\x07','').replace('\r','')
                            설계자 = table.Cell(Row=11, Column=2).Range.Text.replace('\r\x07','').replace('\r','')
                            공사기간 = table.Cell(Row=11, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
                            시공자 = table.Cell(Row=11, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
                            감리자 = table.Cell(Row=15, Column=3).Range.Text.replace('\r\x07','').replace('\r','')

                            facility.facility_address = 시설물주소
                            facility.facility_spec = 시설물종류

                            facility.facility_class = 시설물종별
                            facility.facility_category = 시설물구분

                            facility.facility_architect = 설계자
                            facility.facility_builder = 시공자
                            facility.facility_supervisor = 감리자

                            facility.facility_constructionPeriod = 공사기간

                        elif cropped_pdf.endswith("_상세제원.pdf"):    
                            tables = doc.Tables
                            table = tables(1)
                            
                            주용도 = table.Cell(Row=2, Column=2).Range.Text.replace('\r\x07','').replace('\r','')

                            basement = table.Cell(Row=5, Column=3).Range.Text.replace('\r\x07','').replace('\r','').replace(' ','')
                            basement = '' if basement == '0층' else basement
                            ground = table.Cell(Row=5, Column=1).Range.Text.replace('\r\x07','').replace('\r','').replace(' ','')
                            층수 = ('지하' + basement + ', ' if basement else '') + '지상' + ground

                            최고높이 = table.Cell(Row=5, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
                            건축면적 = table.Cell(Row=9, Column=3).Range.Text.replace('\r\x07','').replace('\r','')
                            건축연면적 = table.Cell(Row=9, Column=4).Range.Text.replace('\r\x07','').replace('\r','')
                            구조형식 = table.Cell(Row=7, Column=1).Range.Text.replace('\r\x07','').replace('\r','')

                            facility.facility_width_building = 건축면적
                            facility.facility_width_gross = 건축연면적
                            facility.facility_structure = 구조형식 
                            facility.facility_floor = 층수
                            facility.facility_usage = 주용도

                        # elif cropped_pdf.endswith("_진단이력.pdf"):        
                        #     tables = doc.Tables
                        #     for num_tbl, table in enumerate(tables, start=1):
                        #         if num_tbl == 1:
                        #             continue

                        
                        # 사용승인일, 건설기간, 건설시작일, 종료일, 준공후경과년수
                        # facility.facility_buildingDate = 준공일
                        
                        # facility.facility_constructStartAt = models.DateField(null=True)
                        # facility.facility_constructEndAt = models.DateField(null=True)

                        # 대지면적, 건축면적, 연면적, 구조형식
                        #facility.facility_width_land= 

                        facility.save()
                        print("종료")

                        doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)
                    except Exception as e:
                        print(e)
                        doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)

                self.word.Quit()  
            except Exception as e:
                print(e)
                self.word.Quit()  

            for file in os.listdir(cropped_pdf_folder):
                os.remove(os.path.join(cropped_pdf_folder, file))



    def createWord():
        import pythoncom
        pythoncom.CoInitialize()
        excel = WordApp()
        pythoncom.CoUninitialize()

    thread = Thread(target = createWord)
    thread.start()

    map = Map.objects.get(map = basic)
    worker = Worker.objects.filter(worker=basic).order_by("id")
    context = {
        'basic' : basic,
        'map' : map,
        'worker' : worker,
    }
    return render(req, 'main/file.html', context)


def IsFileReady(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)

    facility = Facility.objects.get(facility=basic)
    if facility.facility_spec == '-' :
        resultBool = False
    else :
        resultBool = True

    redirect_url = reverse("main:file", args=(resultBool,))
    return JsonResponse({"redirect_url": redirect_url})

def Common(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    contract = Contract.objects.get(contract=basic)
    facility = Facility.objects.get(facility=basic)

    if req.method=='POST': 
        print(req.POST)

        contract.contract_name =req.POST['contract_name']
        contract.contract_method =req.POST['contract_method']
        contract.contract_agency =req.POST['contract_agency']
        contract.contract_money =req.POST['contract_money']
        contract.save()

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
        facility.facility_constructStartAt = req.POST['facility_constructStartAt']
        facility.facility_constructEndAt = req.POST['facility_constructEndAt']
        facility.facility_buildingDate = req.POST['facility_buildingDate']
        facility.facility_old = req.POST['facility_old']
        facility.save()

        redirect_url = reverse("main:picture", args=(basic_id,))
        return JsonResponse({"redirect_url": redirect_url})

    else : 
        context = {
            'basic': basic,
            'contract': contract,
            'facility': facility,
        }
        return render(req, 'main/common.html', context)

def Picture(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    context = {
            'basic': basic,
        }
    return render(req, 'main/picture.html', context)