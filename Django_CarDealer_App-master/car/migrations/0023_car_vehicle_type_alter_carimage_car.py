# Generated by Django 5.1.1 on 2024-10-23 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0022_carimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='vehicle_type',
            field=models.CharField(default='Sedan', max_length=25),
        ),
        migrations.AlterField(
            model_name='carimage',
            name='car',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='car.car'),
        ),
    ]
