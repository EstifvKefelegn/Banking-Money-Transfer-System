from django import forms 
from .models import KYC
from django.forms import ImageField, FileInput, DateInput

class DateInput(forms.DateInput):
    input_type = "date"

class KYCForms(forms.ModelForm):
    identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    signature = ImageField(widget=FileInput)

    class Meta:
        model = KYC
        fields = ['fullname', 'image', 'maritial_status', 'gender', 'identity_type', 'identity_image', 'date_of_birth', 'signature', 'country','state', 'city', 'mobile','fax'] 
        widgets ={
            "fullname": forms.TextInput(attrs={"placeholder":"Full Name"}),
            "mobile": forms.TextInput(attrs={'placeholder':"Mobile Number"}),
            "fax": forms.TextInput(attrs={"placeholder":"Fax Number"}),
            "country": forms.TextInput(attrs={"placeholder": "Country"}),
            "state": forms.TextInput(attrs={"placeholder":"state"}),
            "city": forms.TextInput(attrs={"placeholder":'city'}),
            "date_of_birth": DateInput
        }   