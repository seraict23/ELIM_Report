from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Previous_report(BaseModel):
    Location:str
    Date:int
    Hangeul_file:str
    Excel_file:str
    # Filepaths must include r at the beginning

@app.post("/이전_보고서_업로드")
def Upload_previous_report(previous_report: Previous_report):
    import win32com.client as win32

    hwp=win32.Dispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL","SecurityModule")
    # Must have the same name "SecurityModule"
    hwp.Open(previous_report.Hangeul_file,'','')
    