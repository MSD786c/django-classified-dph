# Generated by Django 3.1.2 on 2021-04-07 11:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_title', models.CharField(max_length=100)),
                ('make_year', models.IntegerField()),
                ('make_month', models.CharField(max_length=100)),
                ('car_manufacturer', models.CharField(max_length=100)),
                ('car_model', models.CharField(max_length=100)),
                ('car_version', models.CharField(max_length=100)),
                ('car_color', models.CharField(max_length=100)),
                ('fuel_type', models.CharField(choices=[('lpg', 'LPG'), ('cng', 'CNG'), ('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric')], default='petrol', max_length=25)),
                ('transmission_type', models.CharField(choices=[('automatic', 'Automatic'), ('manual', 'Manual')], default='manual', max_length=25)),
                ('car_owner', models.CharField(choices=[('first owner', 'First Owner'), ('second owner', 'Second Owner'), ('third owner', 'Third Owner'), ('fourth owner or more', 'Fourth Owner or More')], default='first owner', max_length=25)),
                ('kilometer_driven', models.IntegerField()),
                ('expected_selling_price', models.IntegerField()),
                ('registration_type', models.CharField(choices=[('individual', 'Individual'), ('corporate', 'Corporate'), ('taxi', 'Taxi')], default='individual', max_length=25)),
                ('insurance_type', models.CharField(choices=[('comprehensive', 'Comprehensive'), ('third party', 'Third Party'), ('expired', 'Expired')], default='expired', max_length=25)),
                ('registration_number', models.CharField(max_length=30)),
                ('car_description', models.TextField()),
                ('car_post_date', models.DateField(default=datetime.datetime.now)),
                ('car_photo', models.ImageField(upload_to='car/car_images/')),
                ('car_status', models.CharField(choices=[('active', 'Active'), ('deactive', 'Deactive')], default='active', max_length=25)),
                ('vehicle_type', models.CharField(choices=[('vehicle', 'Vehicle'), ('agriculture_instrument', 'Agriculture_instrument')], default='vehicle', max_length=25)),
                ('car_owner_phone_number', models.IntegerField(default=0)),
                ('car_city', models.CharField(default='-', max_length=50)),
                ('car_owner_name', models.CharField(default='-', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('car_title',),
            },
        ),
    ]
