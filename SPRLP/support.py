import datetime
import json
from string import Template

from django.core.mail import send_mail

from .models import *


class DateStorage:
    def __init__(self, got_date, got_date_url):
        self.date = got_date
        self.date_url = got_date_url


class TaskStorage:
    def __init__(self, got_id, got_name, got_is_assigned, got_ustn):
        self.id = got_id
        self.name = got_name
        self.is_assigned = got_is_assigned
        self.ustn = got_ustn


class UstnStorage:
    def __init__(self, got_ustn):
        self.id = got_ustn.id
        self.name = got_ustn.name
        self.tasks = []


def url_to_date(url):
    year = url // 10000 + 2000
    month = url % 10000 // 100
    day = url % 100
    result = datetime.date(year, month, day)
    return result


def msg_handler(msg_type, email, user=CustomUser(first_name="",last_name="",surname=""), code="", asi_task=Assignment(task=Task())):
    with open('SPRLP/media/SPRLP/responses.json', 'r', encoding="utf-8") as outfile:
        data = json.load(outfile)
        for keyval in data:
            if keyval['id'] == msg_type:
                mail_text = keyval["message"]
                mail_text_template = Template(mail_text)
                response=mail_text_template.safe_substitute(first_name=user.first_name, last_name=user.last_name, surname=user.surname,
                                              group=user.groups.all().exclude(name="Студент")[0].name, code=code,
                                              task_name=asi_task.task.name, task_date=asi_task.date)
    if msg_type == 1:
        title = "Активация записи на практикум"
    elif msg_type == 2:
        title = "Успешная запись на практикум"
    elif msg_type == 3:
        title = "Ваша запись на практикум была отменена"
    else:
        title = "Ваша учетная запись была верифицирована"
    return send_mail(title,
                     response,
                     "ka910238@gmail.com",
                     [email])
