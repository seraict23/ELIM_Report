import os
import win32com.client as win32
import sqlite3
from pathlib import Path
from table_maker import tableMaker


BASE_DIR = Path(__file__).resolve().parent.parent
PATH = str(BASE_DIR)+"/src/hwp_templates"

hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.XHwpWindows.Item(0).Visible = True
hwp.RegisterModule(
    "FilePathCheckDLL", "FilePathCheckerModuleExample")

hwp.Open(PATH+"/2-2 시설물 사용 및 관리실태.hwp", "HWP", "forceopen:true")

myList = ['지하1층', '주차장 및 기타실 일부', '118.11', '주차 관제실', '118.11', '2007.02.15', 
          '지상14층', '미용실', '199.2', '제2종근린생활시설(체력단련장)', '199.2','2022.03.15']

hwp = tableMaker(hwp, 'hi', 2, 6, myList)

hwp.SaveAs(PATH + '/' +'임시저장.hwp')

hwp.Quit()
