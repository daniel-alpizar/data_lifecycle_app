# Generated by Django 4.2.6 on 2023-11-15 23:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coffeeshop", "0008_alter_datawarehouse_customer_id_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="datawarehouse",
            options={"verbose_name_plural": "Datawarehouse"},
        ),
        migrations.AlterField(
            model_name="datawarehouse",
            name="customer_id",
            field=models.IntegerField(default=47, editable=False),
        ),
        migrations.AlterField(
            model_name="rawdata",
            name="customer_id",
            field=models.IntegerField(default=19, editable=False),
        ),
    ]