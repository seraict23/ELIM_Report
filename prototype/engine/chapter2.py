import win32com.client as win32


import threading
import pythoncom

from .func import openhwp, fielder, saveAndQuit, tableMaker


class Worker(threading.Thread):
    def __init__(self, input):
        self.dict = input
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        dict=self.dict

        hwp = openhwp("2-2 시설물 사용 및 관리실태", True)

        try:
            # valueDict={
            #     'usagechange':1,
            #     'structurechange':2, 
            #     'environmentchange':1
            # }
            # mapDict = {
            #     'usage':'usagechangeext', 
            #     'structure':'structurechangeext', 
            #     'environment':'environmentchangeext'
            # }
            # factionList = ['usagechange', 'structurechange', 'environmentchange']

            # for i in factionList:
            #     if valueDict[i]==1:
            #         valueDict[i+'ext']='▣유, □무, □불명'
            #     elif valueDict[i]==2:
            #         valueDict[i+'ext']='□유, ▣무, □불명'
            #     else:
            #         valueDict[i+'ext']='□유, □무, ▣불명'

            # hwp = fielder(hwp, mapDict, valueDict)

            # myList = ['지하1층', '주차장 및 기타실 일부', '118.11', '주차 관제실', '118.11', '2007.02.15', '',
            # '지상14층', '미용실', '199.2', '제2종근린생활시설(체력단련장)', '199.2','2022.03.15','']

            # hwp = tableMaker(hwp, 'hi', 2, 7, myList)


            # 용도변경
            row = dict['usagechange-row']
            list = dict['usagechange-list']

            hwp = tableMaker(hwp, 'startpoint1', row, 7, list)

            # 구조변경
            row = dict['structurechange-row']
            list = dict['structurechange-list']

            hwp = tableMaker(hwp, 'startpoint2', row, 7, list)

            # 주변환경
            row = dict['environmentchange-row']
            list = dict['environmentchange-list']

            hwp = tableMaker(hwp, 'startpoint3', row, 3, list, False)


            saveAndQuit(hwp, "테스트용임시저장3")

        except Exception as e:
            print(e)
            hwp.Quit()



        # 사용 후 uninitialize
        pythoncom.CoUninitialize()











