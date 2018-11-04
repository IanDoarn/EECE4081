# Generated by Django 2.1.3 on 2018-11-04 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pool', '0011_auto_20181030_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonalSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pool.Season')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bet',
            name='has_paid_for_season',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bet',
            name='has_paid_for_week',
            field=models.BooleanField(default=False),
        ),
    ]
