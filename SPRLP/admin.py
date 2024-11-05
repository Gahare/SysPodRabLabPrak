import json
import os

import django
from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.template.response import TemplateResponse
from django.urls import path

from .models import *
from .forms import ResponseMessageForm, UserAdminForm


class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Письма автоматических рассылок",
                "app_label": "Письма автоматических рассылок",
                # "app_url": "/admin/test_view",
                "models": [
                    {
                        "name": "Письмо потдверждения записи",
                        "object_name": "Письмо потдверждения записи",
                        # "admin_url": "/admin/mail_confirm",
                        "admin_url": "/admin/response_msg/1",

                    },
                    {
                        "name": "Письмо успешной записи",
                        "object_name": "Письмо успешной записи",
                        # "admin_url": "/admin/mail_success",
                        "admin_url": "/admin/response_msg/2",

                    },
                    {
                        "name": "Письмо отмены записи",
                        "object_name": "Письмо отмены записи",
                        # "admin_url": "/admin/mail_cancel",
                        "admin_url": "/admin/response_msg/3",

                    },
                    {
                        "name": "Письмо верификации регистрации",
                        "object_name": "Письмо верификации регистрации",
                        # "admin_url": "/admin/mail_approve",
                        "admin_url": "/admin/response_msg/4",

                    }
                ],
            }
        ]
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("response_msg/<int:msg_id>", self.admin_view(self.my_view))]
        temp = my_urls + urls
        return temp

    def my_view(self, request, msg_id):
        context = dict(
            self.each_context(request),
        )
        if request.method == "POST":
            got_form = ResponseMessageForm(request.POST)
            if got_form.is_valid():
                new_text = got_form.cleaned_data['message']
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
                return redirect("/admin/response_msg/" + str(msg_id))
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
        context["form"] = form
        return TemplateResponse(request, "admin/msg_response_edit.html", context)


admin_site = CustomAdminSite()
admin.site = admin_site

# Register your models here.
"""@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()"""


class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "get_ustn"]

    def get_ustn(self, obj):
        return "\n".join([g.name for g in obj.ustn.all()])

    get_ustn.short_description = "Находится в установках"


"""@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("surname", "name", "group")

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()"""

"""@admin.register(UstanovkaAligment)
class UAAdmin(admin.ModelAdmin):
    list_display = ("name", "task")"""


class UstanovkaAdmin(admin.ModelAdmin):
    list_display = ["name", "get_task"]

    def get_task(self, obj):
        return "\n".join([g.name for g in Task.objects.filter(ustn=obj).all()])

    get_task.short_description = "Содержит задания"
    # def save_model(self, request, obj, form, change):
    #    pass
    """obj.save()

        for item in UstanovkaAligment.objects.filter(name=obj.name):
            temp = Task()
            temp.name = item.task.name
            temp.date = obj.date
            temp.isTaken = False
            temp.isReviewed = False
            temp.ustanovka = obj
            temp.save()"""


"""@admin.register(TaskAligment)
class TAAdmin(admin.ModelAdmin):
    pass"""


class CUAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "get_group"]

    def get_group(self, obj):
        return "\n".join([g.name for g in obj.groups.all()])

    get_group.short_description = "Группа"

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        obj.save()

    form = UserAdminForm


#    pass


class AAdmin(admin.ModelAdmin):
    list_display = ["__str__", "date"]

    #def add_view(self, request, form_url="", extra_context=None):
    #    self.exclude = ('task', 'student', 'reviewer', 'mark', 'isTaken', 'isReviewed')
    #    return super(AAdmin, self).add_view(request)

    #def change_view(self, request, object_id, form_url="", extra_context=None):
    #    return super(AAdmin, self).change_view(request, object_id)

    #def save_model(self, request, obj, form, change):
    #    if not change:
    #        added_tasks = Task.objects.filter(ustn=obj.ustn)
    #        for i in added_tasks:
    #            to_add = Assignment()
    #            to_add.date = obj.date
    #            to_add.ustn = obj.ustn
    #            to_add.task = i
    #            to_add.student = None
    #            to_add.reviewer = None
    #            to_add.mark = None
    #            to_add.isTaken = False
    #            to_add.isReviewed = False
    #            to_add.save()
    #            return to_add
    #    else:
    #        obj.save()
    #        return obj


# @admin.register(ResponseMessage)
# class RMAdmin(admin.ModelAdmin):
#    form = ResponseMessageForm
#    empty_value_display = "По умолчанию"


admin_site.register(Task, TaskAdmin)
admin_site.register(Ustanovka, UstanovkaAdmin)
admin_site.register(CustomUser, CUAdmin)
admin_site.register(Assignment, AAdmin)
admin_site.register(django.contrib.auth.models.Group)
