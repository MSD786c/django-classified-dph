# Generated by Django 3.2 on 2024-10-01 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0015_auto_20240918_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='vehicle_type',
            field=models.CharField(choices=[('Car', 'Car'), ('Bike', 'Bike')], default='Car', max_length=25),
        ),
    ]
