# Generated by Django 4.2.6 on 2023-11-10 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_delete_customuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="home_store",
            field=models.IntegerField(default=1, editable=False),
        ),
    ]
