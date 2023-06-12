from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from ..models import Basic, Contract, Facility, Worker, UploadFile, Map, PartPhoto, Defect

import os, glob
from pathlib import Path
from pypdf import PdfReader, PdfWriter

import win32com.client as win32
from threading import Thread



def PDFConverter(req, basic_id):

    basic = Basic.objects.get(pk=basic_id)
    uploadFile = UploadFile.objects.get(file=basic)

    FILENAME = req.POST['filename']
    uploadFile.file_name_BML = FILENAME

    debugText = "보임?"

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PATH = str(BASE_DIR)+"\\static\\"
    pdf_folder = os.path.join(PATH, "시설물대장")
    cropped_pdf_folder = os.path.join(PATH, "tmp")

    for pdf in glob.glob(pdf_folder+"\\"+FILENAME):
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

        # 완료 표시
        uploadFile.file_bool_BML = True
        uploadFile.save()

        pythoncom.CoUninitialize()

    thread = Thread(target = createWord)
    thread.start()


    
    context = {
        'basic' : basic,
    }
    return render(req, 'main/file.html', context)



def ExcelData(req, basic_id):
    basic = Basic.objects.get(pk=basic_id)
    uploadFile = UploadFile.objects.get(file = basic)

    fileName = req.POST['filename']
    uploadFile.file_name_EXCEL = fileName
    uploadFile.file_bool_EXCEL = False
    uploadFile.save()

    # DB table 초기화
    Defect.objects.filter(defect = basic).delete()

    # 엑셀 처리
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PATH = str(BASE_DIR)+"\\static\\"
    print(PATH)

    class ExcelApp:
        def __init__(self):
            self.excel = win32.Dispatch("Excel.Application")
            self.excel.Visible = False

            wb = self.excel.WorkBooks.Open(PATH+fileName)
            ws = wb.Sheets("결함리스트")

            # 원하는 범위만큼 셀 읽기

            count = 0
            locationBefore = ""
            for row in range(10, 3000):
                valueList = []
                for col in range(1, 21):
                    valueList.append(str(ws.Cells(row, col).Value))
                if valueList.count("None")>10:
                    print(count, " 종료")
                    break
                else : 
                    print(valueList)
                    photo_number = 'No.'+valueList[14].split('.')[0] if valueList[14]!="None" else ""
                    number = valueList[2].split('.')[0] if valueList[2]!="None" else ""

                    if valueList[1]!="None" and valueList[1]!="":
                        locationBefore = valueList[1]

                    Defect.objects.create(
                        defect = basic,
                        location = valueList[1] if valueList[1]!="None" and valueList[1]!="" else locationBefore,
                        number = number,
                        part = valueList[5],
                        material = valueList[6],
                        shapeType = valueList[7],
                        width = valueList[8],
                        LengthArea = valueList[9],
                        each = valueList[10],
                        progress = valueList[11],
                        note = valueList[12],
                        cause = valueList[13],
                        photoNumber =photo_number,
                        photoName=valueList[18] if valueList[18]!="None" else "",
                    )
                count += 1
            # win32api.MessageBox(0, "완료되었습니다. 새로고침을 누르세요", "확인창", 0)

    def createExcel():
        import pythoncom
        pythoncom.CoInitialize()
        excel = ExcelApp()
        uploadFile.file_bool_EXCEL = True
        uploadFile.save()
        pythoncom.CoUninitialize()

    thread = Thread(target = createExcel)
    thread.start()


    context = {
        'basic' : basic,
    }
    return render(req, 'main/file.html', context)



def FMLTest(req, basic_id):
    print("FML")
    print(req.POST)
    
    basic = Basic.objects.get(pk=basic_id)
    uploadFile = UploadFile.objects.get(file=basic)
    uploadFile.file_name_FML = req.POST['filename']

    uploadFile.file_bool_FML = True
    uploadFile.save()
    context = {
        "basic":basic
    }
    return render(req, 'main/file.html', context)



def DWGTest(req, basic_id):
    print("DWG")
    print(req.POST)
    basic = Basic.objects.get(pk=basic_id)
    uploadFile = UploadFile.objects.get(file=basic)
    uploadFile.file_name_DWG = req.POST['filename']

    uploadFile.file_bool_DWG = True
    uploadFile.save()
    context = {
        "basic":basic
    }
    return render(req, 'main/file.html', context)


def FileReady(req, basic_id, fileType):
    basic = Basic.objects.get(pk=basic_id)
    uploadFile = UploadFile.objects.get(file=basic)
    if fileType == "BML" :
        ready = uploadFile.file_bool_BML
    elif fileType == "FML" :
        ready = uploadFile.file_bool_FML
    elif fileType == "EXCEL" :
        ready = uploadFile.file_bool_EXCEL
    elif fileType == "DWG" :
        ready = uploadFile.file_bool_DWG
    
    redirect_url = reverse("main:file", args=(basic.id,))
    return JsonResponse({"redirect_url": redirect_url, "resultBool": ready})



