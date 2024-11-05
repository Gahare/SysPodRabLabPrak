# Generated by Django 4.1.7 on 2023-05-31 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SPRLP', '0003_responsemessages'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResponseMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1500)),
            ],
        ),
        migrations.DeleteModel(
            name='ResponseMessages',
        ),
    ]
