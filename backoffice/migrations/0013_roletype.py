# Generated by Django 5.0.2 on 2024-08-18 07:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0012_alter_location_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Roletype",
            fields=[
                ("id", models.SmallAutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(blank=True, max_length=2, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("createdat", models.DateTimeField()),
                ("createdby", models.IntegerField()),
                ("modifiedat", models.DateTimeField(blank=True, null=True)),
                ("modifiedby", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "roletype",
                "managed": False,
            },
        ),
    ]
