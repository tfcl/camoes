# Generated by Django 3.1.1 on 2021-03-16 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0002_auto_20210315_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 31, 16, 22, 12, 168565)),
        ),
    ]
