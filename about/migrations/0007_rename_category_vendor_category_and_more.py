# Generated by Django 4.1.7 on 2023-04-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0006_datar_volume'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='Category',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='vendor',
            name='license_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
