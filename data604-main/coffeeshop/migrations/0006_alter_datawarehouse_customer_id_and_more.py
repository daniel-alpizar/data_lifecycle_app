# Generated by Django 4.2.6 on 2023-11-10 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_profile_home_store"),
        ("coffeeshop", "0005_alter_datawarehouse_customer_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datawarehouse",
            name="customer_id",
            field=models.IntegerField(default=15, editable=False),
        ),
        migrations.AlterField(
            model_name="orders",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.profile"
            ),
        ),
        migrations.AlterField(
            model_name="rawdata",
            name="customer_id",
            field=models.IntegerField(default=99, editable=False),
        ),
    ]
