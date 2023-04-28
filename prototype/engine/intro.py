import win32com.client as win32

from .func import openhwp, fielder, imager, saveAndQuit, appendDict

def intro(dict):

    hwp = openhwp("표지1")

    try:
        report_date_Y = str(dict["report_date"]).split('-')[0]
        report_date_M = str(dict["report_date"]).split('-')[1]
        report_date_D = str(dict["report_date"]).split('-')[2]

        paramObj = {
            "report_date_Y": report_date_Y,
            "report_date_MD": report_date_M+"-"+report_date_D,
            "report_date_M": report_date_M
        }

        dict = appendDict(dict, paramObj)

        mapDict = {
            "년도": "report_date_Y",
            "월일": "report_date_MD",
            "목적물": "building_name",
            "월": "report_date_M"
        }

        hwp = fielder(hwp, mapDict, dict)

        building_out_image = dict['building_image']
        hwp = imager(hwp, "{%전경사진%}", building_out_image, 130.0, 80.0)

        saveAndQuit(hwp, "표지1")

    except Exception as e:
        print(e)
        hwp.Quit()


def introMap(dict):
    hwp = openhwp("전경사진")

    try:
        map_image = dict['map_image']
        building_image = dict['building_image']

        hwp = imager(hwp, "{%지도%}", map_image, 145.0, 100.0)
        hwp = imager(hwp, "{%전경사진%}", building_image, 145.0, 100.0)

        saveAndQuit(hwp, "전경사진")

    except Exception as e:
        print(e)
        hwp.Quit()


def resultTable(dict):
    hwp = openhwp("결과표")
   
    try:
        report_date_Y = str(dict["report_date"]).split('-')[0]
        
        report_date_M = str(dict["report_date"]).split('-')[1]
        if int(report_date_M)<7:
            semiannual = "상반기"
        else :
            semiannual = "하반기"
        
        paramObj = {
            "report_date_Y": report_date_Y,
            "semiannual": semiannual
        }

        dict = appendDict(dict, paramObj)

        mapDict = {
            "년도": "report_date_Y",
            "시설물명": "building_name",
            "반기": "semiannual",
            "종별": "building_class",
            "시설물구분": "building_category",
            "공동수급": "contract_joint",
            "계약방법": "contract_method",
            "시설물종류": "building_spec",
            "점검금액": "contract_money",
            # "안전등급": "safety_grade",
            "주소": "building_address",
            "시설물규모": "building_scale"
        }

        hwp = fielder(hwp, mapDict, dict)

        saveAndQuit(hwp, "결과표")

    except Exception as e:
        print(e)
        hwp.Quit()
