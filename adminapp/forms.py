from django import forms
from .models import AdminRegistrationModel


class AdminRegistrationModelForm(forms.ModelForm):
    class Meta:
        model = AdminRegistrationModel
        fields = ['adm_username', 'adm_password', 'adm_email', 'adm_phone']



        widgets = {
            'adm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'adm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'adm_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adm_phone': forms.TextInput(attrs={'class': 'form-control'}),

        }
    def clean_adm_username(self):
        """
        Custom validation method to ensure the uniqueness of the user name.

        Raises:
            forms.ValidationError: If the user name already exists in the database.
        """
        adm_username = self.cleaned_data.get('user_name')
        if AdminRegistrationModel.objects.filter(user_name=adm_username).exists():
            raise forms.ValidationError("Username already exists. Please choose a different one.")
        return adm_username

    def clean_adm_email(self):
        """
        Custom validation method to ensure the uniqueness of the email address.

        Raises:
            forms.ValidationError: If the email address already exists in the database.
        """
        adm_email = self.cleaned_data.get('user_email')
        if AdminRegistrationModel.objects.filter(user_email=adm_email).exists():
            raise forms.ValidationError("Email address already exists. Please use a different one.")
        return adm_email

