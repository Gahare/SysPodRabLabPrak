from django import forms
from django.contrib import admin

from SPRLP.models import CustomUser


class Register(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    surname = forms.CharField(label='Фамилия', max_length=100)
    dadname = forms.CharField(label='Отчество', max_length=100)
    group = forms.CharField(label='Группа', max_length=100)
    email = forms.EmailField(label='Почта', max_length=255)
    login = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput())


class Login(forms.Form):
    login = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput())
    temp = forms.PasswordInput()


class TaskSign(forms.Form):
    surname = forms.CharField(label='Фамилия', max_length=100)
    name = forms.CharField(label='Имя', max_length=100)
    dadname = forms.CharField(label='Отчество', max_length=100)
    group = forms.CharField(label='Группа', max_length=100)
    email = forms.EmailField(label='Почта', max_length=255)


"""class UstanovkaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UstanovkaAdminForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Название'

        temp_choises = []
        formatted_choises = []
        choose = forms.Select()
        ustn = UstanovkaAligment.objects.all()
        for item in ustn:
            if item.name not in temp_choises:
                temp_choises.append(item.name)
        for i in temp_choises:
            temp = [i, i]
            formatted_choises.append(temp)
        choose.choices = formatted_choises

        self.fields['name'].widget = choose"""


class TaskVerification(forms.Form):
    code = forms.CharField(label="Код подтверждения", max_length=7)


class ResponseMessageForm(forms.Form):
    message = forms.CharField(label="Сообщение", max_length=1500, widget=forms.Textarea())


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "surname", "groups", "email", "username", "password"]
        #exclude = ['is_superuser','is_active','last_login','is_staff']
        pass
