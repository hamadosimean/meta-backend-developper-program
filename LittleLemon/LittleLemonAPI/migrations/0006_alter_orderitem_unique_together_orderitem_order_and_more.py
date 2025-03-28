# Generated by Django 5.1.6 on 2025-03-02 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0005_rename_title_category_category_title_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="LittleLemonAPI.order",
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together={("order", "menuitem")},
        ),
    ]
