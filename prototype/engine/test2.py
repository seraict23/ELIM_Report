from pathlib import Path
import win32com.client as win32
from time import sleep

from .func import openhwp, saveAndQuit, tableMaker

import threading
import pythoncom



def statusTable(dict):
    pageNum = 1
    paramDict=[]

    count = 1    
    hwp = openhwp("결함조사 현황표", True)
    for i in dict:
        paramDict.append(i)

        if count==20 :
            hwp = tableMaker_list2d(hwp, 'startpoint', 20, 11, paramDict, False)
            saveAndQuit(hwp, "결함조사 현황표"+str(pageNum))
            paramDict = []
            hwp = openhwp("결함조사 현황표", True)
            count=0
            pageNum+=1

        count+=1
    hwp = tableMaker_list2d(hwp, 'startpoint', len(paramDict), 11, paramDict, False)
    saveAndQuit(hwp, "결함조사 현황표"+str(pageNum))
    
def tableMaker_list2d(hwp, startField, row, col, list2d, newRow = True):
    hwp.MoveToField(startField, False, False, False)

    if (row > 1) and (newRow):
        hwp.HAction.GetDefault("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
        hwp.HParameterSet.HTableInsertLine.Side = hwp.SideType("Bottom")
        hwp.HParameterSet.HTableInsertLine.Count = row-1
        hwp.HAction.Execute("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
    # print(list2d)
    for i in range(row):
        for j in range(col):
            text = list2d[i][j+1]
            hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HParameterSet.HInsertText.Text = text
            hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)

            if (j<col-1):
                hwp.HAction.Run("MoveRight")
            sleep(0.05)

        if (i<row-1) :
            hwp.HAction.Run("MoveDown")
            sleep(0.05)
            hwp.HAction.Run("TableColBegin")
            sleep(0.05)

    return hwp


class Worker(threading.Thread):
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        paramDict = self.dict.copy()

        # 표지
        statusTable(paramDict)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()



