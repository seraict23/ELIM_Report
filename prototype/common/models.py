from django.db import models

# Create your models here.


class Common(models.Model):
    building_name = models.CharField(max_length=64)
    report_date = models.DateField(auto_now=False)
    building_address = models.CharField(max_length=128)
    building_category = models.CharField(max_length=32)
    contract_joint = models.CharField(
        max_length=32,
        choices=[
            ('ALONE', '독자수행'),
            ('JOINT', '협업')
        ],
        default='ALONE'
    )
    contract_method = models.CharField(max_length=32, default="수의계약")
    contract_money = models.IntegerField()
    building_spec = models.CharField(max_length=256)
    building_date = models.DateField()
    building_class = models.CharField(max_length=16)
    building_scale = models.CharField(max_length=128)
    safety_grade = models.CharField(max_length=16)

    # 사진들 (주소)
    building_pic = models.CharField(max_length=256)
    building_map = models.CharField(max_length=256)

    def __str__(self):
        return self.building_name


class Worker(models.Model):
    job = models.ForeignKey(Common, on_delete=models.CASCADE)

    worker_name = models.CharField(max_length=32)

    worker_role = models.CharField(
        max_length=16,
        choices=[
            ("SR", "책임기술자"),
            ("JR", "참여기술자")
        ]

    )

    worker_class = models.CharField(
        max_length=16,
        choices=[
            ("SP", "특급기술자"),
            ("EX", "중급기술자"),
            ("ST", "초급기술자")
        ]
    )

    worker_startDate = models.DateField()

    def __str__(self):
        return self.worker_name


# class Pics():
#     pass
