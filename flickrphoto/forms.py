from django import forms
from .models import UserData
 
class PhotoForm(forms.Form):
    location = forms.CharField(max_length=256)

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['search_key', 'user_ip']
