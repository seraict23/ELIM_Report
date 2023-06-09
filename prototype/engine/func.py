from pathlib import Path
import win32com.client as win32
from time import sleep


def openhwp(filename, boolean=False):
    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = str(BASE_DIR)+"/src/hwp_templates"

    hwp = win32.Dispatch("HWPFrame.HwpObject")
    hwp.XHwpWindows.Item(0).Visible = boolean
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")

    hwp.Open(PATH+"/"+filename+".hwp", "HWP", "forceopen:true")
    return hwp


def fielder(hwp, map: dict, valueDict: dict):
    fieldList = hwp.GetFieldList().split("\x02")
    keyList = map.keys()
    for i in fieldList:
        if i in keyList:
            hwp.PutFieldText(i, valueDict[map[i]])
    return hwp


def imager(hwp, fieldName, imgName, width=70.0, height=65.0):

    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = str(BASE_DIR)+"/src/pics"
    
    print(PATH+"/"+imgName)
    
    hwp.HAction.Run("MoveDocEnd")
    hwp.InsertPicture(PATH+"/" + imgName, Embedded=True)
    sleep(2)
    hwp.FindCtrl()
    hwp.HAction.GetDefault("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)

    # 크기 변경
    hwp.HParameterSet.HShapeObject.Width = hwp.MiliToHwpUnit(width)
    hwp.HParameterSet.HShapeObject.Height = hwp.MiliToHwpUnit(height)
    hwp.HAction.Execute("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)

    # 잘라내서 위치에 붙이기
    hwp.HAction.Run("Cut")
    hwp.HAction.GetDefault("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
    hwp.HParameterSet.HFindReplace.FindString = fieldName
    hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
    hwp.HAction.Execute("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)

    hwp.HAction.GetDefault("Paste", hwp.HParameterSet.HSelectionOpt.HSet)
    hwp.HAction.Execute("Paste", hwp.HParameterSet.HSelectionOpt.HSet)

    return hwp


def saveAndQuit(hwp, fileName):
    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = str(BASE_DIR)+"/src/result"
    hwp.SaveAs(PATH + '/' + fileName+'.hwp')
    hwp.Quit()

    sleep(1)


# 딕셔너리에 키 추가
def appendDict(target:dict, value:dict):
    keyList = value.keys()
    for i in keyList:
        target[i]= value[i]
    return target



# 표만들기
def tableMaker(hwp, startField, row, col, list):
    flag = hwp.MoveToField(startField, False, False, False)

    if row > 1:
        hwp.HAction.GetDefault("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
        hwp.HParameterSet.HTableInsertLine.Side = hwp.SideType("Bottom")
        hwp.HParameterSet.HTableInsertLine.Count = row-1
        hwp.HAction.Execute("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)

    for i in range(row):
        for j in range(col):
            text = list.pop(0)
            hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HParameterSet.HInsertText.Text = text
            hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HAction.Run("MoveRight")
            sleep(0.1)


    return hwp
