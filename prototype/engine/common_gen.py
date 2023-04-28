import os
import win32com.client as win32
import sqlite3
from pathlib import Path

import threading
import pythoncom

from .intro import intro, introMap, resultTable


class Worker(threading.Thread):
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        paramDict = self.dict.copy()

        # 표지
        intro(paramDict)

        # 전경사진, 지도
        introMap(paramDict)

        # 결과표
        resultTable(paramDict)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()
