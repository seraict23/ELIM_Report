import win32com.client as win32

from func import openhwp, fielder, imager, saveAndQuit, appendDict, tableMaker, imagerFielder


hwp = openhwp("부위별사진", True)

mapdict = {
    "내용-1":"a",
    "내용-2":"b",
    "번호-1":"NO.01",
    "번호-2":"NO.02"
}

valuedict={
    "a":"지붕층 헬리포트 현황",
    "b":"지붕층 E/V기계실 현황",
    "NO.01":"NO.01",
    "NO.02":"NO.02"
}

hwp = fielder(hwp, mapdict, valuedict)

hwp = imagerFielder(hwp, '그림-1', '국민은행여의도본점 전경사진.jpg')
