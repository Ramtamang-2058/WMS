# Generated by Django 4.1.7 on 2023-04-24 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0007_rename_category_vendor_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]