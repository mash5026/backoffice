# Generated by Django 5.0.2 on 2024-10-30 10:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0022_alter_customuser_province"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="province",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
