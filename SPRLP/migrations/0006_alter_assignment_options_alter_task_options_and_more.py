# Generated by Django 4.1.7 on 2023-06-06 22:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SPRLP', '0005_delete_responsemessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignment',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AlterField(
            model_name='assignment',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_reviewer', to=settings.AUTH_USER_MODEL),
        ),
    ]
