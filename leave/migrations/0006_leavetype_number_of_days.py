# Generated by Django 3.2.19 on 2024-06-29 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_auto_20240629_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavetype',
            name='Number_of_days',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
