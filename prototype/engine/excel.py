from pathlib import Path
import win32com.client as win32
import win32api

BASE_DIR = Path(__file__).resolve().parent.parent
PATH = str(BASE_DIR)+"/src/"

excel = win32.Dispatch("Excel.Application")
excel.Visible = True

wb = excel.WorkBooks.Open(PATH+"골든튤립에버용인호텔 2023년 상반기 정기안전점검 결함조사리스트.xlsx")
ws = wb.Sheets("결함리스트")

# 원하는 범위만큼 셀 읽기

count = 0
for row in range(10, 3000):
    valueList = []
    for col in range(1, 22):
        valueList.append(str(ws.Cells(row, col).Value))
    count += 1
    if valueList.count("None")>10:
        print(count, " 종료")
        break
    else : 
        print(valueList)

win32api.MessageBox(0, "완료되었습니다..", "확인창", 16)