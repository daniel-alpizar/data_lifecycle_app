# Generated by Django 4.2.6 on 2023-11-10 05:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coffeeshop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datawarehouse",
            name="customer_id",
            field=models.IntegerField(default=80, editable=False),
        ),
        migrations.AlterField(
            model_name="rawdata",
            name="customer_id",
            field=models.IntegerField(default=92, editable=False),
        ),
    ]