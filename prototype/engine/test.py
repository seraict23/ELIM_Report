import os
import win32com.client as win32
import sqlite3
from pathlib import Path

import threading
import pythoncom

from .intro import intro, introMap, resultTable, workerTable


class Worker(threading.Thread):
    def __init__(self, dict, row):
        self.dict = dict
        self.row = row
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        

        workerTable(self.dict, self.row)

        # 사용 후 uninitialize
        pythoncom.CoUninitialize()
