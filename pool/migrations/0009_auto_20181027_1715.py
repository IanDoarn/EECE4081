# Generated by Django 2.1.2 on 2018-10-27 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0008_auto_20181027_1707'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameupload',
            options={'ordering': ['upload_date']},
        ),
    ]
