# Generated by Django 2.1.1 on 2018-10-30 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0002_auto_20181030_0716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='user',
            new_name='user_id',
        ),
    ]
