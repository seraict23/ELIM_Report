import win32com.client as win32

from time import sleep
import copy

import threading
import pythoncom


from .func import openhwp, fielder, saveAndQuit, imageTable, tableMaker_list2d, merger, imagerFielder, tableMaker_1Line, tableMaker_titleLine


class Worker(threading.Thread):
    def __init__(self, input):
        self.list2d = input
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()
        
        # 현황표
        paramList2d = self.list2d
        statusTableB(paramList2d)

        # 결함 현황 사진
        statusPictures(paramList2d)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()


def statusTable(dict):
    pageNum = 1
    paramList=[]

    count = 1    
    hwp = openhwp("결함조사 현황표", True)
    try:
        for i in dict:
            paramList.append(i)

            if count==20 :
                hwp = tableMaker_list2d(hwp, 'startpoint', 20, 11, paramList, False)
                saveAndQuit(hwp, "결함조사 현황표"+str(pageNum))
                paramList = []
                hwp = openhwp("결함조사 현황표", True)
                count=0
                pageNum+=1

            count+=1
        hwp = tableMaker_list2d(hwp, 'startpoint', len(paramList), 11, paramList, False)
        saveAndQuit(hwp, "결함조사 현황표"+str(pageNum))

    except Exception as e:
        print(e)
        hwp.Quit()



def statusTableB(dict):
    pageNum = 1
    count = 1    
    hwp = openhwp("결함조사 현황표", True)

    try:
        for i in dict:

            # 타이틀 설정
            mapDict = {
                "title":"title",
                "number":"number"
            }

            valueDict = {
                "title":"3.2.4 결함조사 현황표",
                "number":str(pageNum)
            }

            if pageNum>0:
                valueDict['title']=''

            hwp = fielder(hwp, mapDict, valueDict)


            # 표 만들기
            isFirstRow = False
            if count == 1:
                isFirstRow = True

            location = i[0]
            row = i[1:12]

            if location != "":
                hwp = tableMaker_titleLine(hwp, location, isFirstRow )
                count+=1
                isFirstRow=False

            hwp = tableMaker_1Line(hwp, 11, row, isFirstRow)

            # 셀병합
            if (row[0] == '') and not(isFirstRow):
                hwp.HAction.Run("MoveUp")
                hwp.HAction.Run("TableCellBlock")
                hwp.HAction.Run("TableCellBlockExtend")
                hwp.HAction.Run("TableUpperCell")
                hwp.HAction.Run("TableMergeCell")
                sleep(0.1)
                hwp.HAction.Run("MoveDown")

            # 종료 조건
            if count==20 :
                saveAndQuit(hwp, "결함조사 현황표"+str(pageNum))
                hwp = openhwp("결함조사 현황표", True)
                count=0
                pageNum+=1
            count+=1
        saveAndQuit(hwp, "결함조사 현황표"+str(pageNum))

    except Exception as e:
        print(e)
        hwp.Quit()
        


def statusPictures(list2d):

    valueList=[]
    for i in list2d:
        if i[11] != '' :
            valueList.append(i)
    
    piccount = len(valueList)
    pagecount = piccount//6+1

    for i in range(1, pagecount+1):
        hwp = openhwp("결함조사 사진 현황", True)

        mapDict = {}
        valueDict={}

        for k in range(1,7):
            if 0<len(valueList) :
                value = valueList.pop(0)
                print(value)

                mapDict['번호-'+str(k)]='번호-'+str(k)
                valueDict['번호-'+str(k)] = value[11]

                mapDict['내용-'+str(k)]='내용-'+str(k)
                valueDict['내용-'+str(k)] = value[0]+' '+value[2]+' '+value[3]+' '+value[4]

                imgFileName = str(value[12].split('.')[0])

                hwp = imagerFielder(hwp, '그림-'+str(k), '20230210_'+imgFileName+'.jpg')

        hwp = fielder(hwp, mapDict, valueDict)

        saveAndQuit(hwp, '결함조사 사진 현황'+str(i))