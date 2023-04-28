import os
import win32com.client as win32
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PATH = str(BASE_DIR)+"/src/hwp_templates"

hwp = win32.Dispatch("HWPFrame.HwpObject")
hwp.XHwpWindows.Item(0).Visible = True
hwp.RegisterModule(
    "FilePathCheckDLL", "FilePathCheckerModuleExample")

hwp.Open(PATH+"/표지1.hwp", "HWP", "forceopen:true")

fieldList = hwp.GetFieldList().split("\x02")
for i in fieldList:
    print(i)
# hwp.PutFieldText(Field=i, Text=dict[i])

# hwp.SaveAs(PATH + '/result/표지1_result.hwp')

hwp.Quit()
