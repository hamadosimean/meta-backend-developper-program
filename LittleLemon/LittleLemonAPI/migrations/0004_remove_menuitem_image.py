# Generated by Django 5.1.6 on 2025-02-26 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "LittleLemonAPI",
            "0003_remove_customuser_bio_remove_customuser_birth_date_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menuitem",
            name="image",
        ),
    ]
