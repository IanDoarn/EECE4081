# Generated by Django 2.1.3 on 2018-12-04 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0013_auto_20181127_1030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bet',
            options={'ordering': ['date_time', 'user']},
        ),
    ]
