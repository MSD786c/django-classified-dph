# Generated by Django 5.1.4 on 2025-01-21 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0029_alter_car_make_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='licenseplate',
            old_name='max_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='licenseplate',
            name='min_price',
        ),
    ]
