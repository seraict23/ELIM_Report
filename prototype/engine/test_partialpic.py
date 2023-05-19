import win32com.client as win32

from .func import openhwp, fielder, imager, saveAndQuit, appendDict, tableMaker, imagerFielder, merger

import os
import sqlite3
from pathlib import Path

import threading
import pythoncom

class Worker(threading.Thread):
    def __init__(self, dict):
        self.dict = dict
        super().__init__()

    def run(self):
        # 서브 스레드에서 COM 객체를 사용하려면 COM 라이브러리를 초기화 해야함
        pythoncom.CoInitialize()

        valueDict = self.dict.copy()

        mapdict={}

        num = int(valueDict['pagecount'])

        for k in range(1, num+1):
            hwp = openhwp("부위별사진", False)      

            pagenum = (k-1)*6 

            for i in range(1, 7):
                id = pagenum+i

                # 내용
                mapdict["내용-"+str(i)]='picture-'+str(id)+'-content'
                if 'picture-'+str(id)+'-content' in valueDict:
                    pass
                else :
                    valueDict['picture-'+str(id)+'-content']='-'

                #번호
                mapdict["번호-"+str(i)]='picture-'+str(id)+'-number'
                if id<10:
                    valueDict['picture-'+str(id)+'-number']="NO.0"+str(id)
                else :
                    valueDict['picture-'+str(id)+'-number']="NO."+str(id)


                # 그림
                fieldName = '그림-'+str(i)
                if 'picture-'+str(id) in valueDict:
                    hwp = imagerFielder(hwp, fieldName, valueDict['picture-'+str(id)])
                else :
                    hwp = imagerFielder(hwp, fieldName, 'default.jpg')            

            hwp = fielder(hwp, mapdict, valueDict)

            saveAndQuit(hwp, '부위별사진'+str(k))

            if k>1 :
                merger('부위별사진'+str(k-1), '부위별사진'+str(k))



        # 사용 후 uninitialize
        pythoncom.CoUninitialize()



