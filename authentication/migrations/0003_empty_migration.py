# Generated by Django 4.0.6 on 2022-08-03 17:04

from django.db import migrations
from authentication.servicies import create_dev_user


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0002_empty_migration"),
    ]

    operations = [migrations.RunPython(create_dev_user)]
