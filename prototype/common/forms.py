from django import forms


from .models import Common


class CommonForm(forms.Form):
    building_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}), label="시설물명")
    report_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "date"}), label="날짜")


class BuilidingForm(forms.ModelForm):

    class Meta:
        model = Common
        fields = ("building_date", "building_address",
                  "building_category", "building_class", "building_spec", "building_scale")
        labels = {"building_date": '준공일', "building_address": '주소',
                  "building_category": '시설물구분', "building_class": '종별',
                  "building_spec": '시설물종류', "building_scale": '시설물규모'}
        widgets = {
            "building_date": forms.DateInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}),
            "building_address": forms.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}),
            "building_category": forms.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}),
            "building_class": forms.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}),
            "building_spec": forms.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}),
            "building_scale": forms.TextInput(attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"})
        }


class ContractForm(forms.Form):
    contract_joint = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}), label="공동수급")
    contract_method = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}), label="계약방법")
    contract_money = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}), label="점검금액")


class BuildingInfoForm(forms.Form):
    building_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}), label="준공일")
    building_address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': "floatingInput", "placeholder": "name"}), label="주소")


BUILDING_CATEGORY_CHOICES = [
    ('1','공동주택 외의 건축물로서 21층 이상 또는 연면적 5만m2 이상의 건축물'),
    ('2','연면적 1만m2이상의 지하도상가 (지하도면적 포함)'),
    ('3','16층 이상의 공동주택'),
    ('4','1종 시설물에 해당하지 않는 공동주택 외의 건축물로서 16층 이상 또는 연면적 3만m2이상의 건축물'),
    ('5','1종 시설물에 해당하지 않는 건축물로서 연면적 5천m2이상의 문화 및 집회시설, 종교시설, 판매시설, 운수시설 중 여객용 시설, 의료시설, 노유자 시설, 수련시설, 운동시설, 숙박시설 중 관광숙박시설 및 관광 휴게시설'),
    ('6','1종 시설물에 해당하지 않는 지하도상가로서 연면적 5천m2 이상의 지하도 상가 (지하보도면적 포함)'),
    ('7','준공 후 15년이 경과된 5층 이상 ~ 15층 이하 아파트'),
    ('8','준공 후 15년이 경과된 연면적 660m2 초과, 4층 이하 연립주택'),
    ('9','준공 후 15년이 경과된 연면적 1천m2 이상~ 5천m2 미만의 판매시설, 숙박시설, 운수시설, 문화 및 집회시설, 의료시설, 장례식장, 종교시설, 위락시설, 관광휴게시설, 수련시설, 노유자시설, 운동시설, 교육시설'),
    ('10','준공 후 15년이 경과된 연면적 5백m2 이상 ~ 1천m2 미만의 문화 및 집회시설 중 공연장 및 집회장, 종교시설, 운동시설'),
    ('11','준공 후 15년이 경과된 연면적 3백m2 이상 ~ 1천m2 미만의 위락시설, 관광휴게시설'),
    ('12','준공 후 15년이 경과된 11층 이상 ~ 16층 미만의 위락시설 또는 연면적 5천m2이상 ~ 3만m2 미만의 건축물'),
    ('13','5천m2 미만의 상가가 설치된 지하도 상가 (지하보도면적 포함)'),
    ('14','준공 후 15년이 경과된 연면적 1천m2 이상의 공공청사')
]


class BuildingCategoryForm(forms.Form):
    building_category = forms.CharField(
        widget=forms.Select(
            choices=BUILDING_CATEGORY_CHOICES,
            attrs={
               "style": "width:600px;text-align:left"
            }
        ), label="시설물구분"
    )
