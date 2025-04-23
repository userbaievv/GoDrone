from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label="Пароль"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label="Подтверждение пароля"
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться', css_class='btn btn-primary w-full mt-4'))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        label="Ник"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        label="Пароль"
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn btn-primary w-full mt-4'))
