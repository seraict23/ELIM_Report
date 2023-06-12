import win32com.client as win32

from .hwp2 import openhwp, fielder, imager, saveAndQuit, appendDict, tableMaker, tableMaker_list2d, imagerFielder

import threading
import pythoncom


def intro(paramDict):
    hwp = openhwp("0-1 표지1", True)

    mapDict={
        "년도": "년도",
        "반기": "반기",
        "월-일": "월-일",
        "건물명": "건물명",
        "전경사진": "전경사진",
        "월": "월",
    }

    valueDict = {
        "년도": paramDict['basic_year'],
        "반기": paramDict['basic_semi'],
        "월-일": paramDict['basic_year']+'-'+paramDict['basic_month'],
        "건물명": paramDict['basic_name'],
        "전경사진": "",
        "월": paramDict['basic_month'],
    }

    print(valueDict) 
    print(mapDict)

    
    hwp = fielder(hwp, mapDict, valueDict)
    hwp = imagerFielder(hwp, '전경사진', paramDict['map_titlePic_name'], 104, 87)
    saveAndQuit(hwp, "0-1 표지1")


    hwp2 = openhwp("0-3 전경사진", True)
    hwp2 = imagerFielder(hwp2, '지도', paramDict['map_map_name'], 158, 95)
    hwp2 = imagerFielder(hwp2, '전경사진', paramDict['map_titlePic_name'], 156, 109)

    saveAndQuit(hwp2, "0-3 전경사진")



def engineers(paramDict):
    hwp = openhwp("0-8 참여기술진", True)

    # 파싱
    paramList = []
    for i in paramDict:
        paramList.append(i['worker_role'])
        workerName = ' '.join(list(i['worker_name']))
        paramList.append(workerName)
        paramList.append(i['worker_class'])
        paramList.append(i['worker_period'])
        paramList.append(i['worker_job'])
        workerNote = i['worker_note'] if i['worker_note'] != "" else "-"
        paramList.append(workerNote)


    row = len(paramList)//6

    hwp = tableMaker(hwp, "startpoint", row, 6, paramList)

    saveAndQuit(hwp, "0-8 참여기술진")



class SecondThread(threading.Thread):
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        paramDict = self.dict.copy()

        # 표지
        engineers(paramDict)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()


class SecondThreadIntro(threading.Thread):
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        paramDict = self.dict.copy()

        # 표지
        intro(paramDict)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()



def resultTable(paramDict):
    hwp=openhwp("0-9 결과표", True)

    engineerList = [
    ]

    mapFields = {
        "용역명":"",
        "점검기간":"",
        "관리주체명":"",
        "공동수급":"",
        "계약방법":"",
        "종류":"",
        "구분":"",
        "종별":"",
        "준공일":"",
        "금액":"",
        "등급":"",
        "주소":"",
        "규모":"",
        "시설물명":"",
        "startpoint":"",
        "참여기술진":"",
    }

    for i in list(mapFields.keys()):
        mapFields[i]=i
    print(mapFields)

    valueDict = paramDict

    hwp = fielder(hwp, mapFields, valueDict)

    engineerList = paramDict['engineers']
    col = len(engineerList)//4

    hwp = tableMaker(hwp, "startpoint", col, 4, engineerList, False)

    saveAndQuit(hwp, "0-9 결과표")



class SecondThreadResultTable(threading.Thread):
    pass
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        paramDict = self.dict.copy()

        # 결과표
        resultTable(paramDict)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()