from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255, help_text='Название должности')

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, default=None)

    SEX = (
        ('м', 'Мужской'),
        ('ж', 'Женский'),
        ('н', 'Не указано'),
    )

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=SEX, blank=True, default='н')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    record_book_id = models.CharField(max_length=7, null=True, blank=True)
    passport_id = models.CharField(max_length=11, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.RESTRICT)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return '{0} {1}'.format(self.position, self.full_name)

    def get_absolute_url(self):
        return reverse('employee-detail', args=(str(self.id)))


class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    WEEKDAY_LIST = (
        ('пн', 'Понедельник'),
        ('вт', 'Вторник'),
        ('ср', 'Среда'),
        ('чт', 'Четверг'),
        ('пт', 'Пятница'),
        ('сб', 'Суббота'),
        ('вс', 'Воскресенье'),
    )

    weekday = models.CharField(max_length=2, choices=WEEKDAY_LIST)
    work_start_time = models.TimeField()
    work_end_time = models.TimeField()

    class Meta:
        ordering = ['employee', 'weekday']

    def __str__(self):
        return '{0}, {1}: {2}-{3}'.format(self.employee, self.weekday, self.work_start_time, self.work_end_time)


class Specialization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.RESTRICT)

    def __str__(self):
        return '{0}: {1}'.format(self.employee, self.specialization)

    def get_absolute_url(self):
        return reverse('doctor-detail', args=[str(self.id)])


class Office(models.Model):
    office_number = models.CharField(max_length=4)

    def __str__(self):
        return self.office_number


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)
    office = models.ManyToManyField(Office)
    doctor = models.ManyToManyField(Doctor)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service-detail', args=[str(self.id)])


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, default=None)

    SEX = (
        ('м', 'Мужской'),
        ('ж', 'Женский'),
        ('н', 'Не указано'),
    )

    class Meta:
        ordering = ['full_name']

    full_name = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=70, default='')
    gender = models.CharField(max_length=1, choices=SEX, blank=True, default='н')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    passport_id = models.CharField(max_length=11, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Пациент ' + self.full_name


class MedicalTest(models.Model):
    date = models.DateTimeField()
    name = models.CharField(max_length=255)
    result = models.CharField(max_length=1000)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date', 'name']

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.date)


class Appointment(models.Model):
    date = models.DateTimeField()
    patient_complaints = models.CharField(max_length=1000, null=True, blank=True)
    anamnesis = models.CharField(max_length=1000, null=True, blank=True)
    examination_result = models.CharField(max_length=1000, null=True, blank=True)
    diagnosis = models.CharField(max_length=1000, null=True, blank=True)
    recommendations = models.CharField(max_length=1000, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-date', 'doctor']

    def __str__(self):
        return 'Прием у {0} ({1})'.format(self.doctor, self.date)
