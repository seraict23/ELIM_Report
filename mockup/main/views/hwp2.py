from pathlib import Path
import win32com.client as win32
from time import sleep


def openhwp(filename, boolean=False):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PATH = str(BASE_DIR)+"/static/hwp_templates"

    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.XHwpWindows.Item(0).Visible = boolean
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")

    hwp.Open(PATH+"/"+filename+".hwp", "HWP", "forceopen:true")
    return hwp


def fielder(hwp, map: dict, valueDict: dict):
    fieldList = hwp.GetFieldList().split("\x02")
    keyList = map.keys()
    print(fieldList)
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
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PATH = str(BASE_DIR)+"/static/result"
    hwp.SaveAs(PATH + '/' + fileName+'.hwp')
    hwp.Quit()

    sleep(1)


# 딕셔너리에 키 추가
def appendDict(target:dict, value:dict):
    keyList = value.keys()
    for i in keyList:
        target[i]= value[i]
    return target


# 표 새로 만들기
def newTable(hwp):
    return hwp


# 표 작성 하기 : 일렬 리스트일때
def tableMaker(hwp, startField, row, col, list, newRow = True):
    hwp.MoveToField(startField, False, False, False)

    if (row > 1) and (newRow):
        hwp.HAction.GetDefault("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
        hwp.HParameterSet.HTableInsertLine.Side = hwp.SideType("Bottom")
        hwp.HParameterSet.HTableInsertLine.Count = row-1
        hwp.HAction.Execute("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
    print(list)
    for i in range(row):
        for j in range(col):
            text = list.pop(0)
            print(text)
            hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HParameterSet.HInsertText.Text = text
            hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)

            if (j<col-1):
                hwp.HAction.Run("MoveRight")
            sleep(0.05)

        if (i<row-1) :
            hwp.HAction.Run("MoveDown")
            sleep(0.05)
            hwp.HAction.Run("TableColBegin")
            sleep(0.05)

    return hwp

# 표 작성 2차원 배열
def tableMaker_list2d(hwp, startField, row, col, list2d, newRow = True):
    hwp.MoveToField(startField, False, False, False)

    if (row > 1) and (newRow):
        hwp.HAction.GetDefault("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
        hwp.HParameterSet.HTableInsertLine.Side = hwp.SideType("Bottom")
        hwp.HParameterSet.HTableInsertLine.Count = row-1
        hwp.HAction.Execute("TableInsertRowColumn", hwp.HParameterSet.HTableInsertLine.HSet)
    # print(list2d)
    for i in range(row):
        for j in range(col):
            text = list2d[i][j+1]
            hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
            hwp.HParameterSet.HInsertText.Text = text
            hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)

            if (j<col-1):
                hwp.HAction.Run("MoveRight")
            sleep(0.02)

        if (i<row-1) :
            hwp.HAction.Run("MoveDown")
            sleep(0.05)
            hwp.HAction.Run("TableColBegin")
            sleep(0.05)

    return hwp

def tableMaker_1Line(hwp, col, list, firstRow=False, startField='startpoint'):
    if firstRow:
        hwp.MoveToField(startField, False, False, False)

    for j in range(col):
        text = list[j]
        hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
        hwp.HParameterSet.HInsertText.Text = text
        hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
        sleep(0.05)
        if (j<col-1):
            hwp.HAction.Run("MoveRight")
            sleep(0.02)

    try:
        hwp.HAction.Run("MoveDown")
        sleep(0.05)
        hwp.HAction.Run("TableColBegin")
        sleep(0.05)
    except Exception as e:
        print(e)

    return hwp


def tableMaker_titleLine(hwp, text, firstRow=False, startField='startpoint'):
    try:
        if firstRow:
            hwp.MoveToField(startField, True, False, False)

        hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
        hwp.HParameterSet.HInsertText.Text = text
        hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
        hwp.HAction.Run("TableCellBlock")
        hwp.HAction.Run("TableCellBlockRow")
        hwp.HAction.Run("TableMergeCell")
        hwp.HAction.Run("ParagraphShapeAlignLeft")
        sleep(0.7)
        
        hwp.HAction.Run("MoveDown")
        hwp.HAction.Run("TableColEnd")
        hwp.HAction.Run("TableColBegin")
        
    except Exception as e:
        print(e)

    return hwp


# 이미지테이블
def imageTable(hwp, positionName, imgList:list, width=75.0, height=65.0):

    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = str(BASE_DIR)+"/src/pics"

    for imgName in imgList:
        hwp.InsertPicture(PATH+"/" + imgName, Embedded=True)
        sleep(0.5)
        hwp.FindCtrl()

        # 크기 변경
        hwp.HAction.GetDefault("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)
        hwp.HParameterSet.HShapeObject.Width = hwp.MiliToHwpUnit(width)
        hwp.HParameterSet.HShapeObject.Height = hwp.MiliToHwpUnit(height)
        hwp.HAction.Execute("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)

        # 잘라내서 위치에 붙이기
        hwp.HAction.Run("Cut")
        hwp.HAction.GetDefault("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)
        hwp.HParameterSet.HFindReplace.FindString = positionName
        hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        hwp.HAction.Execute("RepeatFind", hwp.HParameterSet.HFindReplace.HSet)

        hwp.HAction.GetDefault("Paste", hwp.HParameterSet.HSelectionOpt.HSet)
        hwp.HAction.Execute("Paste", hwp.HParameterSet.HSelectionOpt.HSet)

        sleep(0.1)
        hwp.HAction.Run("MoveRight")

    return hwp

def imagerFielder(hwp, fieldName, imgName, width=75.0, height=65.0):

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PATH = str(BASE_DIR)+"/static/img/temp"
    
    print(PATH+"/"+imgName)
    
    hwp.MoveToField(fieldName, True, False, False)
    hwp.InsertPicture(PATH+"/" + imgName, Embedded=True)
    sleep(0.5)
    hwp.FindCtrl()

    # 크기 변경
    hwp.HAction.GetDefault("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)
    hwp.HParameterSet.HShapeObject.Width = hwp.MiliToHwpUnit(width)
    hwp.HParameterSet.HShapeObject.Height = hwp.MiliToHwpUnit(height)
    hwp.HAction.Execute("ShapeObjDialog", hwp.HParameterSet.HShapeObject.HSet)

    return hwp


# 머지
def merger(sFile, oFile):

    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = str(BASE_DIR)+"/src/result/"

    hwp = win32.Dispatch("HWPFrame.HwpObject")
    hwp.XHwpWindows.Item(0).Visible = False
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")

    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample")
    hwp.Open(PATH+sFile+".hwp","HWP","forceopen:true")
    hwp.HAction.Run("MoveDocEnd")

    hwp.HAction.GetDefault("InsertFile", hwp.HParameterSet.HInsertFile.HSet)
    option=hwp.HParameterSet.HInsertFile
    option.filename = PATH+oFile+".hwp"
    option.KeepSection = 1
    option.KeepCharshape = 1
    option.KeepParashape = 1
    option.KeepStyle = 1
    hwp.HAction.Execute("InsertFile", hwp.HParameterSet.HInsertFile.HSet)
    
    new_filename = sFile +".hwp"
    new_file_path = PATH+new_filename
    hwp.SaveAs(new_file_path)
    hwp.Quit()


def multiMerge():
    pass




def Header():
    # function OnScriptMacro_script24()
    # {
    #     HAction.GetDefault("HeaderFooter", HParameterSet.HHeaderFooter.HSet);
    #     with (HParameterSet.HHeaderFooter)
    #     {
    #         HSet.SetItem("HeaderFooterStyle", 0);
    #         HSet.SetItem("HeaderFooterCtrlType", 0);
    #     }
    #     HAction.Execute("HeaderFooter", HParameterSet.HHeaderFooter.HSet);
    #     HAction.GetDefault("InsertText", HParameterSet.HInsertText.HSet);
    #     HParameterSet.HInsertText.Text = "용인에버그린아파트";
    #     HAction.Execute("InsertText", HParameterSet.HInsertText.HSet);
    #     HAction.Run("BreakPara");
    #     HAction.Run("DeleteBack");
    #     HAction.Run("CloseEx");
    # }
    pass