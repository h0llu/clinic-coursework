from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from .models import Position, Employee, Schedule, Specialization, \
    Doctor, Office, Service, Patient, MedicalTest, Appointment


class PatientSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, help_text='Имя')
    last_name = forms.CharField(max_length=50, help_text='Фамилия')
    patronymic = forms.CharField(max_length=50, help_text='Отчество')

    GENDER_LIST = (
        ('н', 'не указано'),
        ('м', 'мужской'),
        ('ж', 'женский'),
    )

    gender = forms.ChoiceField(choices=GENDER_LIST, help_text='Пол')
    phone_number = forms.CharField(max_length=15, required=False, help_text='Номер телефона')
    address = forms.CharField(max_length=255, required=False, help_text='Адрес фактического проживания')
    passport_id = forms.CharField(max_length=11, required=False, help_text='Паспортные данные (в виде 0000-000000)')
    birth_date = forms.DateField(required=False, help_text='Дата рождения',
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(max_length=254, help_text='Электронная почта')

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'patronymic',
                  'gender', 'birth_date', 'address', 'passport_id', 'phone_number',
                  'email', 'password1', 'password2',)


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_active', 'date_joined']


class AppointmentCreateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['patient_complaints', 'anamnesis', 'examination_result', 'diagnosis', 'recommendations']


class MedicalTestCreateForm(forms.ModelForm):
    class Meta:
        model = MedicalTest
        exclude = ['result']
