from pathlib import Path
import win32com.client as win32
from time import sleep

def tableMaker(hwp, col, row, list):
    fieldList = hwp.GetFieldList(0, '0x01')
    print(fieldList)
    flag = hwp.MoveToField(fieldList, False, False, False)
    print(flag)

    if row > 1:
        hwp.HAction.GetDefault("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
        hwp.HParameterSet.HTableInsertLine.Side = hwp.SideType("Bottom")
        hwp.HParameterSet.HTableInsertLine.Count = row-1
        hwp.HAction.Execute("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
        print("행 추가 됨?")

    for i in range(row):
        count = 0
        for j in range(col):
            
            text = list.pop(0)
            hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HParameterSet.HInsertText.Text = text
            hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HAction.Run("MoveRight")
            count+=1
            print(count, "/", col)
            if count == col:
                print("right?")
                sleep(0.1)
                hwp.HAction.Run("MoveRight")

    return hwp

def dictParser():
    pass
    