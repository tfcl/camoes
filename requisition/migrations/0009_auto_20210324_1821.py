# Generated by Django 3.1.1 on 2021-03-24 17:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0008_auto_20210324_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 8, 18, 21, 27, 371026)),
        ),
    ]
