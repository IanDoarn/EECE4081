# Generated by Django 2.1.1 on 2018-10-30 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0006_auto_20181030_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='season',
            name='start',
            field=models.DateField(),
        ),
    ]