# Generated by Django 2.1.2 on 2018-10-27 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0006_auto_20181023_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_data', models.FileField(upload_to='')),
            ],
        ),
    ]