import datetime

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from .forms import PatientSignUpForm, PatientForm, EmployeeForm, UserUpdateForm, \
    AppointmentCreateForm, MedicalTestCreateForm
from .models import Position, Employee, Specialization, \
    Doctor, Service, Patient, MedicalTest, Appointment


def index(request):
    num_services = Service.objects.count()
    num_doctors = Doctor.objects.count()
    num_patients = Patient.objects.count()

    doctor_list = Doctor.objects.filter()[:5]
    service_list = Service.objects.filter()[:3]

    return render(request,
                  'index.html',
                  context={'num_services': num_services,
                           'num_doctors': num_doctors,
                           'num_patients': num_patients,
                           'doctor_list': doctor_list,
                           'service_list': service_list})


def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            patronymic = form.cleaned_data.get('patronymic')
            gender = form.cleaned_data.get('gender')
            birth_date = form.cleaned_data.get('birth_date')
            passport_id = form.cleaned_data.get('passport_id')
            phone_number = form.cleaned_data.get('phone_number')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            patient_group = Group.objects.get(name='Пациент')
            patient_group.user_set.add(user)

            new_patient = Patient(
                user=user,
                full_name=last_name + ' ' + first_name + ' ' + patronymic,
                gender=gender,
                birth_date=birth_date,
                passport_id=passport_id,
                phone_number=phone_number,
                email=email,
            )

            new_patient.save()
            return redirect('/')
    else:
        form = PatientSignUpForm()
    return render(request, '../templates/registration/signup.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Пациент').exists())
def personal(request):
    pk = request.user.patient.id
    patient = get_object_or_404(Patient, pk=pk)

    appointments = patient.appointment_set.all()
    medical_tests = patient.medicaltest_set.all()

    return render(request, 'personal.html',
                  {'appointment_list': appointments,
                   'medicaltest_list': medical_tests,
                   'patient': patient})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Администратор').exists() or
                  u.groups.filter(name='Врач').exists())
def patient_personal(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    appointments = patient.appointment_set.all()
    medical_tests = patient.medicaltest_set.all()

    return render(request, 'personal.html',
                  {'appointment_list': appointments,
                   'medicaltest_list': medical_tests,
                   'patient': patient})


class AppointmentDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentDetailView, self).get_context_data(**kwargs)
        datetime_now = datetime.datetime.now()
        context.update({'datetime': datetime_now})
        return context

    def test_func(self):
        appointment = get_object_or_404(Appointment, pk=self.kwargs.get('pk'))

        is_patient = self.request.user.groups.filter(name='Пациент').exists()
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()
        return (is_patient and self.request.user.patient == appointment.patient) or is_admin or is_doctor


class AppointmentUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    fields = '__all__'
    template_name = 'appointment_update.html'
    success_url = '/'

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()

        return is_admin or is_doctor


class AppointmentCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm
    template_name = 'appointment_create.html'
    success_url = '/'

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()

        return is_admin or is_doctor


class MedicalTestDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = MedicalTest
    template_name = 'medicaltest_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MedicalTestDetailView, self).get_context_data(**kwargs)
        datetime_now = datetime.datetime.now()
        context.update({'datetime': datetime_now})
        return context

    def test_func(self):
        medical_test = get_object_or_404(MedicalTest, pk=self.kwargs.get('pk'))

        is_patient = self.request.user.groups.filter(name='Пациент').exists()
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()
        return (is_patient and self.request.user.patient == medical_test.patient) or is_admin or is_doctor


class MedicalTestUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MedicalTest
    fields = '__all__'
    template_name = 'medicaltest_update.html'
    success_url = '/'

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()

        return is_admin or is_doctor


class MedicalTestCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MedicalTest
    form_class = MedicalTestCreateForm
    template_name = 'medicaltest_create.html'
    success_url = '/'

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()

        return is_admin or is_doctor


class UserListView(generic.ListView):
    model = get_user_model()
    template_name = 'user_list.html'
    paginate_by = 10


class UserCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = 'user_create.html'
    success_url = '/users/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'user_update.html'
    success_url = '/users/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class ServiceListView(generic.ListView):
    model = Service
    template_name = 'service_list.html'
    paginate_by = 10


class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'service_detail.html'


class ServiceUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields = '__all__'
    template_name = 'service_update.html'
    success_url = '/services/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class ServiceCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    fields = '__all__'
    template_name = 'service_create.html'
    success_url = '/services/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class DoctorListView(generic.ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    paginate_by = 10


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'


class DoctorUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctor
    fields = '__all__'
    template_name = 'doctor_update.html'
    success_url = '/doctors/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class DoctorCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Doctor
    fields = '__all__'
    template_name = 'doctor_create.html'
    success_url = '/doctors/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class PositionListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Position
    template_name = 'position_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class PositionUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Position
    fields = '__all__'
    template_name = 'position_update.html'
    success_url = '/positions'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class PositionCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Position
    fields = '__all__'
    template_name = 'position_create.html'
    success_url = '/positions'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class SpecializationListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Specialization
    template_name = 'specialization_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class SpecializationUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Specialization
    fields = '__all__'
    template_name = 'specialization_update.html'
    success_url = '/specializations/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class SpecializationCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Specialization
    fields = '__all__'
    template_name = 'specialization_create.html'
    success_url = '/specializations/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class PatientListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Patient
    template_name = 'patient_list.html'
    paginate_by = 10

    def test_func(self):
        is_admin = self.request.user.groups.filter(name='Администратор').exists()
        is_doctor = self.request.user.groups.filter(name='Врач').exists()

        return is_admin or is_doctor


class PatientUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient_update.html'
    success_url = '/patients/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class PatientCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'patient_create.html'
    success_url = '/patients/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Employee
    template_name = 'employee_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class EmployeeUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_update.html'
    success_url = '/employees/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()


class EmployeeCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    fields = '__all__'
    template_name = 'employee_create.html'
    success_url = '/employees/'

    def test_func(self):
        return self.request.user.groups.filter(name='Администратор').exists()
