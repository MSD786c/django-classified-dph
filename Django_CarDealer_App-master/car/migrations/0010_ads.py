# Generated by Django 3.1.2 on 2021-04-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0009_privacy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popup_ad', models.ImageField(upload_to='car/car_images/')),
                ('ad1', models.ImageField(upload_to='car/car_images/')),
                ('ad2', models.ImageField(upload_to='car/car_images/')),
            ],
        ),
    ]
