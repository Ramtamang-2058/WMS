# Generated by Django 4.1.7 on 2023-04-23 23:46

import about.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_remove_vendor_profile_alter_vendor_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='license_photo',
            field=models.ImageField(blank=True, null=True, upload_to=about.models.upload_license_picture),
        ),
    ]
