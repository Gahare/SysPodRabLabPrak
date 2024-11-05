from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dadname = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.surname + " " + self.name

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    dadname = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    approved = models.BooleanField()

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.surname + " " + self.name


class TaskAligment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'


class UstanovkaAligment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    task = models.ForeignKey(TaskAligment, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача в установке'
        verbose_name_plural = 'Задачи в установках'
"""


class CustomUser(AbstractUser):
    surname = models.CharField(max_length=255, null=True)


class Ustanovka(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Установка'
        verbose_name_plural = 'Установки'


class Task(models.Model):
    name = models.CharField(max_length=255)
    ustn = models.ManyToManyField(Ustanovka)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name


class Assignment(models.Model):
    date = models.DateField()
    ustn = models.ForeignKey(Ustanovka, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, blank=True,
                                related_name="assigned_student")
    reviewer = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="assigned_reviewer")
    mark = models.IntegerField(null=True, blank=True)
    isTaken = models.BooleanField()
    isReviewed = models.BooleanField()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.ustn.name + "-" + self.task.name

    def clean(self):
        clean_task = self.task
        clean_ustn = clean_task.ustn.all()
        if self.ustn not in clean_ustn:
            raise ValidationError("Не существует установки с такой задачей")


class VerificationCodes(models.Model):
    code = models.CharField(max_length=7)
    attempting_student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment_link = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField()


# class ResponseMessage(models.Model):
#    type = models.CharField(max_length=100)
#    message = models.CharField(max_length=1500)


class ActionLog(models.Model):
    type = models.CharField(max_length=50)
    applier = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="log_applier")
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="log_receiver")
    assigment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True)
    action_time = models.DateTimeField()
