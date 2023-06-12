from django.db import models

# Create your models here.

class Basic(models.Model):
    basic_name = models.CharField(max_length=64)
    basic_startAt = models.DateField()
    basic_endAt = models.DateField()

    # 자동생성(시작일, 종료일로 결정되는 정보들)
    basic_year = models.CharField(max_length=8)
    basic_month = models.CharField(max_length=8)
    basic_semi = models.CharField(max_length=8)

    def __str__(self):
        return self.basic_name


class Contract(models.Model):
    contract = models.ForeignKey(Basic, on_delete=models.CASCADE)
    # 건축물명 + 년도 + 반기 + 정기안전점검
    contract_name = models.CharField(max_length=64)
    contract_agency = models.CharField(max_length=64)
    contract_joint = models.CharField(max_length=16, default="독자수행100%")
    contract_method = models.CharField(max_length=32, default="수의계약")
    contract_money = models.CharField(max_length=16)
    
    def __str__(self):
        return self.contract_name

# 시설물 관리대장
class Facility(models.Model):
    facility = models.ForeignKey(Basic, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=64)
    facility_address = models.CharField(max_length=64)

    facility_spec = models.CharField(max_length=64, blank=True)

    # 둘다 spec에 종속?
    facility_class = models.CharField(max_length=8, blank=True)
    facility_category = models.CharField(max_length=16, default="건축물")

    facility_architect = models.CharField(max_length=32, blank=True)
    facility_builder = models.CharField(max_length=32, blank=True)
    facility_supervisor = models.CharField(max_length=32, blank=True)
    
    #사용승인일, 건설기간, 건설시작일, 종료일, 준공후경과년수
    facility_buildingDate = models.DateField(null=True, blank=True)
    facility_constructionPeriod = models.CharField(max_length=32, blank=True)
    facility_constructStartAt = models.DateField(null=True, blank=True)
    facility_constructEndAt = models.DateField(null=True, blank=True)
    facility_old = models.CharField(max_length=16, blank=True)

    #대지면적, 건축면적, 연면적, 구조형식
    facility_width_land= models.CharField(max_length=16, blank=True)
    facility_width_building = models.CharField(max_length=16, blank=True)
    facility_width_gross = models.CharField(max_length=16, blank=True)
    facility_structure = models.CharField(max_length=32, blank=True)

    # 건축물 관리대장 층수(동수)
    facility_floor = models.CharField(max_length=32, blank=True)

    facility_usage = models.CharField(max_length=32, blank=True)


    def __str__(self):
        return self.facility_name


class Worker(models.Model):
    worker = models.ForeignKey(Basic, on_delete=models.CASCADE)
    worker_name = models.CharField(max_length=32)
    worker_role = models.CharField(max_length=16)
    worker_class = models.CharField(max_length=16)

    # basic.startAt ~ basic.endAt
    worker_period = models.CharField(max_length=32)

    # worker_role 에 종속
    worker_job = models.CharField(max_length=64)

    # 비고
    worker_note = models.CharField(max_length=32, default="")

    def __str__(self):
        return self.worker_name



class UploadFile(models.Model):
    file = models.ForeignKey(Basic, on_delete=models.CASCADE)
    file_name_BML = models.CharField(max_length=64)
    file_bool_BML = models.BooleanField(default=False)
    file_name_FML = models.CharField(max_length=64)
    file_bool_FML = models.BooleanField(default=False)
    file_name_EXCEL = models.CharField(max_length=64)
    file_bool_EXCEL = models.BooleanField(default=False)
    file_name_DWG = models.CharField(max_length=64)
    file_bool_DWG = models.BooleanField(default=False)
    

class Map(models.Model):
    map = models.ForeignKey(Basic, on_delete=models.CASCADE)
    map_titlePic_name =models.CharField(max_length=32)
    map_titlePic_path =models.CharField(max_length=128)
    map_map_name =models.CharField(max_length=32)
    map_map_path =models.CharField(max_length=128)

    def __str__(self):
        return self.map_titlePic_name
    

class PartPhoto(models.Model):
    partPhoto = models.ForeignKey(Basic, on_delete=models.CASCADE)
    partPhoto_number = models.IntegerField()
    partPhoto_name = models.CharField(max_length=32)
    partPhoto_path = models.CharField(max_length=128)
    partPhoto_note = models.CharField(max_length=128)

    def __str__(self):
        return self.partPhoto_name