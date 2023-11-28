# Generated by Django 4.2.6 on 2023-11-27 18:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeeshop', '0011_alter_datawarehouse_customer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='orders',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
