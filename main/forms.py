from django import forms
from users.models import Profile


class UserCreationProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country']
