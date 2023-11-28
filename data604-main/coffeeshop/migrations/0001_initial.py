# Generated by Django 4.2.6 on 2023-11-10 05:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customers",
            fields=[
                ("customer_id", models.AutoField(primary_key=True, serialize=False)),
                ("home_store", models.IntegerField(default=1, editable=False)),
                ("customer_name", models.CharField(max_length=100)),
                ("customer_email", models.EmailField(blank=True, max_length=100)),
                ("customer_since", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Customers",
            },
        ),
        migrations.CreateModel(
            name="Products",
            fields=[
                ("product_id", models.AutoField(primary_key=True, serialize=False)),
                ("product_group", models.CharField(max_length=20)),
                ("product_category", models.CharField(max_length=20)),
                ("product_type", models.CharField(max_length=40)),
                ("product", models.CharField(max_length=40)),
                ("unit_of_measure", models.CharField(max_length=10)),
                ("current_retail_price", models.FloatField()),
            ],
            options={
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="Rawdata",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transaction_id", models.IntegerField()),
                ("transaction_date", models.DateField(auto_now_add=True)),
                (
                    "transaction_time",
                    models.TimeField(default=django.utils.timezone.now, editable=False),
                ),
                ("customer_id", models.IntegerField(default=42, editable=False)),
                ("order", models.IntegerField(default=1, editable=False)),
                ("quantity", models.IntegerField()),
                ("unit_price", models.FloatField()),
                ("line_item_amount", models.FloatField(editable=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coffeeshop.products",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Rawdata",
            },
        ),
        migrations.CreateModel(
            name="Orders",
            fields=[
                ("transaction_id", models.AutoField(primary_key=True, serialize=False)),
                ("transaction_date", models.DateField(auto_now_add=True)),
                (
                    "transaction_time",
                    models.TimeField(default=django.utils.timezone.now, editable=False),
                ),
                ("order", models.IntegerField(default=1, editable=False)),
                ("quantity", models.IntegerField()),
                ("unit_price", models.FloatField()),
                ("line_item_amount", models.FloatField(editable=False)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coffeeshop.customers",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coffeeshop.products",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="DataWarehouse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("transaction_id", models.IntegerField()),
                ("transaction_date", models.DateField(auto_now_add=True)),
                (
                    "transaction_time",
                    models.TimeField(default=django.utils.timezone.now, editable=False),
                ),
                ("customer_id", models.IntegerField(default=20, editable=False)),
                ("order", models.IntegerField(default=1, editable=False)),
                ("quantity", models.IntegerField()),
                ("unit_price", models.FloatField()),
                ("line_item_amount", models.FloatField(editable=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coffeeshop.products",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "DataWarehouse",
            },
        ),
    ]