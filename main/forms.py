from django import forms
from users.models import Profile


class UserCreationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'phone']
        widgets = {'phone': forms.NumberInput(attrs={'aria-label': 'Sizing example input', 'aria-describedby': 'nputGroup-sizing-default',
                                                     'class': 'form-control'})}
