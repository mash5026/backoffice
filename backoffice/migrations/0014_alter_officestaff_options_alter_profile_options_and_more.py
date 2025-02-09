# Generated by Django 5.0.2 on 2024-08-20 11:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0013_roletype"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="officestaff",
            options={
                "managed": False,
                "verbose_name": "اداره",
                "verbose_name_plural": "ادارات سازمانی",
            },
        ),
        migrations.AlterModelOptions(
            name="profile",
            options={
                "managed": False,
                "verbose_name": "پروفایل",
                "verbose_name_plural": "پروفایل",
            },
        ),
        migrations.AlterModelOptions(
            name="profilerole",
            options={
                "managed": False,
                "verbose_name": "نقش پروفایل",
                "verbose_name_plural": "نقش های پروفایل",
            },
        ),
    ]
