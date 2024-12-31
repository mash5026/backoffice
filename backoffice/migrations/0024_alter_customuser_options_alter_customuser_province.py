# Generated by Django 5.0.2 on 2024-10-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0023_alter_customuser_province"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={"verbose_name": "کاربر", "verbose_name_plural": "کاربران"},
        ),
        migrations.AlterField(
            model_name="customuser",
            name="province",
            field=models.BigIntegerField(blank=True, null=True, verbose_name="شهر"),
        ),
    ]
