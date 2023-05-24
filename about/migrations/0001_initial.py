# Generated by Django 4.1.7 on 2023-04-23 06:28

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dustbin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('dob', models.CharField(blank=True, max_length=255, null=True)),
                ('current_address', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('citizenship_front', models.ImageField(blank=True, null=True, upload_to='')),
                ('citizenship_back', models.ImageField(blank=True, null=True, upload_to='')),
                ('license_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('vehicle_brand', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicle_color', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=255, null=True)),
                ('Category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='about.category')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('True', 'True'), ('False', 'False')], max_length=255, null=True)),
                ('dustbin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='about.dustbin')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
