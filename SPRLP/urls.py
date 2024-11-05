from django.urls import path
from django.contrib.auth import views as auth_views
import datetime

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.sys_login),
    path('register/', views.sys_register),
    path('profile/', views.sys_profile),
    path('<int:date_id>', views.schedule),
    path('task/<int:task_id>', views.task),
    path('profile/cancel/<int:task_id>', views.cancel),
    path('profile/evaluate', views.evaluate),
    path('profile/approve', views.approve_register),
    path('confirm/<int:task_id>', views.approve_task_assigment),
]
