import os
import win32com.client as win32
import sqlite3
from pathlib import Path

import threading
import pythoncom

from ..func import openhwp, fielder, imager, saveAndQuit, appendDict


class Worker(threading.Thread):
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        paramDict = self.dict.copy()

        hwp = openhwp("표지1")

        try:
            report_date_Y = str(self.dict["report_date"]).split('-')[0]
            report_date_M = str(self.dict["report_date"]).split('-')[1]
            report_date_D = str(self.dict["report_date"]).split('-')[2]

            paramObj = {
                "report_date_Y": report_date_Y,
                "report_date_MD": report_date_M+"-"+report_date_D,
                "report_date_M": report_date_M
            }

            paramDict = appendDict(paramDict, paramObj)

            mapDict = {
                "년도": "report_date_Y",
                "월일": "report_date_MD",
                "목적물": "building_name",
                "월": "report_date_M"
            }

            hwp = fielder(hwp, mapDict, paramDict)

            building_out_image = paramDict['building_image']
            hwp = imager(hwp, "{%전경사진%}", building_out_image, 130.0, 80.0)

            saveAndQuit(hwp, "표지1")

        except Exception as e:
            print(e)
            hwp.Quit()


        # 사용 후 uninitialize
        pythoncom.CoUninitialize()
