# Generated by Django 3.2.19 on 2024-06-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0009_auto_20240629_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='start_day',
            field=models.DateField(null=True),
        ),
    ]
