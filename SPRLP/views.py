import codecs
import locale
import operator
import os.path
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import *
import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from collections import defaultdict
from .support import *

from django.template import loader
from .forms import *
import json


# Create your views here.
def index(request):
    # temp = open("SPRLP/media/myfile.txt", "x")
    today1 = datetime.date.today()
    temp = today1
    dates = []
    # send_mail("Subject here",
    #          "Here is the message.",
    #          "ka910238@gmail.com",
    #          ["prohorshubenkov12@gmail.com"])
    #
    for i in range(7):
        temp = temp + datetime.timedelta(days=1)
        temp2 = (temp.year - 2000) * 10000 + temp.month * 100 + temp.day
        temp3 = DateStorage(temp, temp2)
        dates.append(temp3)
    return render(request, 'SPRLP/index.html', {"dates": dates})


def sys_login(request):
    if request.user.is_authenticated:
        return redirect("/profile")
    form = Login()
    response = ""
    if request.method == "POST":
        got_form = Login(request.POST)
        if got_form.is_valid():
            got_login = got_form.cleaned_data['login']
            got_password = got_form.cleaned_data['password']
            cur_user = authenticate(username=got_login, password=got_password)
            if cur_user is not None:
                login(request, cur_user)
                return redirect("/profile")
            else:
                response = "Неверные данные"
            """if CustomUser.objects.filter(username=got_login).exists():
                
                cur_user = CustomUser.objects.get(username=got_login)
                
                if check_password(got_password, cur_user.password):
                    request.session["isLoggedIn"] = True
                    request.session["userType"] = "teacher"
                    request.session["userId"] = Teacher.objects.get(login=got_login).id
                    return redirect("/profile")
                else:
                    response = "Неверные данные"
            else:
                try:
                    Student.objects.get(login=got_login)
                except:
                    response = "Неверные данные"
                    return render(request, 'SPRLP/login.html', {"form": form, "response": response})
                std = Student.objects.get(login=got_login)
                if check_password(got_password, std.password):
                    if std.approved:
                        request.session["isLoggedIn"] = True
                        request.session["userType"] = "student"
                        request.session["userId"] = Student.objects.get(login=got_login).id
                        return redirect("/profile")
                    else:
                        response = "Пользователь не проверен"
                else:
                    response = "Неверные данные"""""
    return render(request, 'SPRLP/login.html', {"form": form, "response": response})


"""
def unlogin(request):
    del request.session["isLoggedIn"]
    del request.session["userType"]
    del request.session["userId"]
    return redirect("/")

"""


def sys_register(request):
    form = Register()
    response = ""
    if request.method == "POST":
        got_form = Register(request.POST)
        if got_form.is_valid():
            got_name = got_form.cleaned_data['name']
            got_surname = got_form.cleaned_data['surname']
            got_dadname = got_form.cleaned_data['dadname']
            got_group = got_form.cleaned_data['group']
            got_email = got_form.cleaned_data['email']
            got_login = got_form.cleaned_data['login']
            got_password = got_form.cleaned_data['password']
            if CustomUser.objects.filter(username=got_login).exists():
                response = "Логин должен быть уникальным"
            elif CustomUser.objects.filter(first_name=got_name,last_name=got_surname,surname=got_dadname):
                response = "Студент с такими данными уже существует"
            else:
                to_add = CustomUser(first_name=got_name, last_name=got_surname,
                                    surname=got_dadname, email=got_email,
                                    username=got_login, is_active=False)
                to_add.set_password(got_password)
                to_add.save()
                to_add_group = Group.objects.get(name="Студент")
                to_add.groups.add(to_add_group.id)
                if Group.objects.filter(name=got_group).exists():
                    to_add_group = Group.objects.get(name=got_group)
                    to_add.groups.add(to_add_group.id)
                    to_add.save()
                else:
                    new_group = Group(name=got_group)
                    new_group.save()
                    to_add_group = Group.objects.get(name=got_group)
                    to_add.groups.add(to_add_group.id)
                    to_add.save()
                response = "Регистрация отправлена на рассмотрение"

    return render(request, 'SPRLP/register.html', {"form": form, "response": response})


"""
"""


@login_required
def sys_profile(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    if request.user.groups.filter(name="Студент").exists():
        user = request.user  # CustomUser.objects.get(id=request.session["userId"])
        future_tasks = Assignment.objects.filter(student=user, date__gt=datetime.date.today())
        future_tasks_list = list(future_tasks)
        previous_tasks = Assignment.objects.filter(student=user, date__lte=datetime.date.today())
        previous_tasks_list = list(previous_tasks)
        previous_tasks_list.sort(key=lambda x:x.date)
        return render(request, 'SPRLP/profile_student.html', {"user": user, "previous": previous_tasks_list,
                                                              "future": future_tasks_list})
    elif request.user.groups.filter(name="Преподаватель").exists():
        user = request.user
        tasks_to_review = Assignment.objects.filter(date__lte=datetime.date.today(), isReviewed=False,
                                                    student__isnull=False)
        tasks_to_review_list = list(tasks_to_review)
        reviewed_tasks = Assignment.objects.filter(date__lte=datetime.date.today(), isReviewed=True)
        reviewed_tasks_list = list(reviewed_tasks)
        users_to_review = CustomUser.objects.filter(is_active=False)
        return render(request, 'SPRLP/profile_teacher.html',
                      {"user": user, "current": tasks_to_review_list,
                       "past": reviewed_tasks_list, "approve": users_to_review})
    return render(request, 'SPRLP/profile_teacher.html', {"user": request.user})


def schedule(request, date_id):
    try:
        result = url_to_date(date_id)
    except ValueError:
        result = datetime.date(1, 1, 1)
    date_response = None
    if result <= datetime.date.today() or result > datetime.date.today() + datetime.timedelta(days=7):
        response = False
        relayed_tasks = None
    else:
        response = True
        locale.setlocale(locale.LC_ALL, 'ru_ru')
        date_response = result.strftime("%B %d")
        """relayed_ustn = []
        relayed_tasks = []
        db_tasks = Ustanovka.objects.filter(date=result).values("id", "name", "isTaken")
        tasks = list(db_tasks)
        for item in tasks:
            temp_task = TaskStorage(item['id'], item['name'], item['isTaken'], item['ustanovka'])
            relayed_tasks.append(temp_task)
        sorted(relayed_tasks, key=operator.attrgetter("name"))
        # создание списка установок
        for i in relayed_tasks:
            if any(temp.id == i.ustn for temp in relayed_ustn):
                for x in relayed_ustn:
                    if x.id == i.ustn:
                        x.tasks.append(i)
                        break
            else:
                a = UstnStorage(i.ustn)
                a.tasks.append(i)
                relayed_ustn.append(a)"""
        relayed_tasks = []
        relayed_ustn = []
        db_assignments = Assignment.objects.filter(date=result)
        assignments = list(db_assignments)
        # создание списка установок
        for i in assignments:
            if any(temp.id == i.ustn.id for temp in relayed_ustn):
                for x in relayed_ustn:
                    if x.id == i.ustn.id:
                        x.tasks.append(i)
                        break
            else:
                a = UstnStorage(i.ustn)
                a.tasks.append(i)
                relayed_ustn.append(a)
    return render(request, 'SPRLP/schedule.html', {"response": response, "ustanovkas": relayed_ustn,
                                                   "dateResponse": date_response})


def task(request, task_id):
    active_assignment = Assignment.objects.get(id=task_id)
    form = TaskSign()
    if active_assignment.isTaken:
        response = "На это задание уже записан студент"
    else:
        form = TaskSign()
        if request.user is not None:
            if request.user.groups.filter(name="Студент").exists():
                active_user = CustomUser.objects.get(id=request.user.id)
                form.fields['surname'].initial = active_user.last_name
                form.fields['name'].initial = active_user.first_name
                form.fields['dadname'].initial = active_user.surname
                all_groups = active_user.groups.all().exclude(name="Студент")
                cur_group = all_groups[0]
                form.fields['group'].initial = cur_group.name
                form.fields['email'].initial = active_user.email
        response = ""
        if request.method == "POST":
            got_form = TaskSign(request.POST)
            if got_form.is_valid():
                got_name = got_form.cleaned_data['name']
                got_surname = got_form.cleaned_data['surname']
                got_dadname = got_form.cleaned_data['dadname']
                got_group = got_form.cleaned_data['group']
                got_email = got_form.cleaned_data['email']
                if CustomUser.objects.filter(first_name=got_name, last_name=got_surname, surname=got_dadname).exists():
                    assigned_student = CustomUser.objects.get(first_name=got_name, last_name=got_surname,
                                                              surname=got_dadname)
                    check_group = assigned_student.groups.all().exclude(name="Студент")
                    cur_check_group = check_group[0].name
                    if assigned_student.email == got_email and cur_check_group == got_group:
                        if not assigned_student.is_active:
                            response = "Студент не верифицирован"
                            return render(request, 'SPRLP/task_assigment.html', {"form": form, "response": response})
                        today_tasks = Assignment.objects.filter(date=active_assignment.date)
                        list(today_tasks)
                        for i in today_tasks:
                            if i.student == assigned_student:
                                response = "Студент уже записан на задание в этот день"
                                return render(request, 'SPRLP/task_assigment.html',
                                              {"form": form, "response": response})

                        ver_code = VerificationCodes()
                        ver_code.code = random.randint(1000000, 9999999)
                        now_time = datetime.datetime.now()
                        delta_time = datetime.timedelta(minutes=5)
                        ver_code.expiration_time = now_time + delta_time
                        ver_code.assignment_link = active_assignment
                        ver_code.attempting_student = assigned_student
                        msg_handler(1, assigned_student.email, assigned_student, str(ver_code.code))
                        ver_code.save()
                        return redirect("/confirm/" + str(ver_code.id))

                    else:
                        response = "Студента с такими данными не существет"

    return render(request, 'SPRLP/task_assigment.html', {"form": form, "response": response})


@login_required
def cancel(request, task_id):
    if request.method == "POST":
        got_form = request.POST
        if got_form['postConf'] == '1':
            delete_task = Assignment.objects.get(id=task_id)
            delete_student = CustomUser.objects.get(id=request.user.id)
            if delete_task.isTaken and delete_task.student == delete_student:
                ustn = delete_task.ustn
                taken_tasks = Assignment.objects.filter(ustn=ustn)
                for i in taken_tasks:
                    i.isTaken = False
                    i.save()
                delete_task.isTaken = False
                delete_task.student = None
                delete_task.save()
                msg_handler(3, delete_student.email, delete_student, "", delete_task)
                log = ActionLog()
                log.type = "Отмена записи на занятие"
                log.applier = delete_student
                log.assigment = delete_task
                log.action_time = datetime.datetime.now()
                log.save()

                return redirect("/profile")
    return render(request, 'SPRLP/cancel.html')


@login_required
def evaluate(request):
    if request.method == "POST":
        got_form = request.POST
        for evaul in got_form:
            if evaul == "csrfmiddlewaretoken":
                pass
            elif got_form[evaul] != "none":
                to_evaluate = Assignment.objects.get(id=int(evaul))
                to_evaluate.isReviewed = True
                to_evaluate.reviewer = request.user
                to_evaluate.mark = int(got_form[evaul])
                to_evaluate.save()

                log = ActionLog()
                log.type = "Оценка занятия"
                log.applier = request.user
                log.receiver = to_evaluate.student
                log.assigment = to_evaluate
                log.action_time = datetime.datetime.now()
                log.save()
        return redirect("/profile")
    to_evaluate = Assignment.objects.filter(isReviewed=False, isTaken=True, student__isnull=False,
                                            date__lte=datetime.date.today())
    to_evaluate_list = list(to_evaluate)
    return render(request, 'SPRLP/evaulate.html', {"tasks": to_evaluate_list})


@login_required
def approve_register(request):
    if request.method == "POST":
        got_form = request.POST
        for approve in got_form:
            if approve == "csrfmiddlewaretoken":
                pass
            elif got_form[approve] != "none":
                to_evaluate = CustomUser.objects.get(id=int(approve))
                if got_form[approve] == "Yes":
                    to_evaluate.is_active = True
                    to_evaluate.save()
                    msg_handler(4, to_evaluate.email, to_evaluate)
                    log = ActionLog()
                    log.type = "Регистрация студента"
                    log.applier = request.user
                    log.receiver = to_evaluate
                    log.action_time = datetime.datetime.now()
                    log.save()

                elif got_form[approve] == "No":
                    to_delete_groups = to_evaluate.groups
                    for i in to_delete_groups.all():
                        if i.name != "Студент":
                            to_delete_groups_students = CustomUser.objects.filter(groups=i)

                            if to_delete_groups_students.count() == 1:
                                i.delete()
                    to_evaluate.delete()
        return redirect("/profile")
    to_approve = CustomUser.objects.filter(is_active=False)
    to_approve_list = list(to_approve)
    return render(request, 'SPRLP/approve.html', {"approve": to_approve_list})


def approve_task_assigment(request, task_id):
    response = ""
    if request.method == "POST":
        got_form = TaskVerification(request.POST)
        if got_form.is_valid():
            code = got_form.cleaned_data["code"]
            activation = VerificationCodes.objects.get(id=task_id)
            if code == activation.code:
                if activation.expiration_time > timezone.now():
                    if not activation.assignment_link.isTaken:
                        active_assignment = activation.assignment_link
                        cur_ustn = active_assignment.ustn
                        taken_tasks = Assignment.objects.filter(ustn=cur_ustn, date=active_assignment.date)
                        for i in taken_tasks:
                            i.isTaken = True
                            i.save()
                        active_assignment.student = activation.attempting_student
                        active_assignment.isTaken = True
                        active_assignment.save()
                        log = ActionLog()
                        log.type = "Запись на занятие"
                        log.applier = activation.attempting_student
                        log.assigment = active_assignment
                        log.action_time = datetime.datetime.now()
                        log.save()
                        msg_handler(2, active_assignment.student.email, active_assignment.student, "",
                                    active_assignment)
                        return redirect("/")
                    else:
                        response = "На задание уже записан студент"
                else:
                    response = "Код подтверждения устарел"
            else:
                response = "Код подтверждения неверен"
    ver_form = TaskVerification()

    return render(request, 'SPRLP/confirm_assignment.html', {"form": ver_form, "response": response})


"""@login_required
def edit_response_message(request, msg_id):
    if request.user.is_superuser:
        if request.method == "POST":
            got_form = ResponseMessageForm(request.POST)
            if got_form.is_valid():
                new_text=got_form.cleaned_data['message']
                with open('SPRLP/media/SPRLP/responses.json', 'r', encoding="utf-8") as outfile:
                    data = json.load(outfile)
                    for keyval in data:
                        if keyval['id'] == msg_id:
                            keyval["message"] = new_text
                outfile.close()
                with open('SPRLP/media/SPRLP/responses.json', 'w', encoding="utf-8") as outfile:
                    json_string = json.dumps(data, ensure_ascii=False)
                    outfile.write(json_string)
                    outfile.close()
                return redirect("/admin")
        if not os.path.isfile('SPRLP/media/SPRLP/responses.json'):
            data = [
                {
                    'id': 1,
                    'type': 'Подтверждение записи',
                    'message': 'Ваш код подтверждения записи: ',
                },
                {
                    'id': 2,
                    'type': 'Успешная запись',
                    'message': 'Вы были записаны на занятие',
                },
                {
                    'id': 3,
                    'type': 'Отмена записи',
                    'message': 'Ваша запись на занятие было отменена',
                },
                {
                    'id': 4,
                    'type': 'Верификация регистрации',
                    'message': 'Ваша регистрация была подтверждена',
                },
            ]
            json_string = json.dumps(data, ensure_ascii=False)
            with open("SPRLP/media/SPRLP/responses.json", "w", encoding="utf-8") as outfile:
                outfile.write(json_string)
                outfile.close()

        with open('SPRLP/media/SPRLP/responses.json', 'r', encoding="utf-8") as outfile:
            data = json.load(outfile)
        form = ResponseMessageForm()
        for keyval in data:
            if keyval['id'] == msg_id:
                form.fields["message"].initial = keyval['message']

        return render(request, 'SPRLP/edit_response_message.html', {"form": form})
    else:
        return redirect("/profile")"""
