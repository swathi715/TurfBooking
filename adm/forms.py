from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'profile-input'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'profile-input'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'profile-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'profile-input'
            }),
        }