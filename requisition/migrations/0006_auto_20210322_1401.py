# Generated by Django 3.1.1 on 2021-03-22 13:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0005_auto_20210320_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 14, 1, 19, 833195)),
        ),
    ]
