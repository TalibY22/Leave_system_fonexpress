# Generated by Django 3.2.19 on 2024-06-29 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_aprroved_leave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='leave_balancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_days', models.IntegerField()),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='leave.employee')),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.leavetype')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='leave.branch'),
            preserve_default=False,
        ),
    ]
