# Generated by Django 4.1.7 on 2023-03-13 21:26

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
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message_body', models.TextField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('read', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('room_num', models.IntegerField()),
                ('admission_wt', models.DecimalField(decimal_places=2, max_digits=5)),
                ('usual_wt', models.IntegerField()),
                ('height', models.IntegerField()),
                ('admission_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='WeightSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reweighed', models.BooleanField(default=False)),
                ('refused', models.BooleanField(default=False)),
                ('not_in_room', models.BooleanField(default=False)),
                ('daily_wts', models.BooleanField(default=False)),
                ('show_alert', models.BooleanField(default=False)),
                ('scale_type', models.CharField(max_length=50, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_field', to='weighttrackingapi.employee')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_sheet', to='weighttrackingapi.resident')),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.DecimalField(decimal_places=1, max_digits=5, null=True)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident_weight', to='weighttrackingapi.resident')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_message', to='weighttrackingapi.message')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='weighttrackingapi.employee')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='weighttrackingapi.employee')),
            ],
        ),
    ]
