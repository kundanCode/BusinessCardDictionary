# Generated by Django 4.2.3 on 2023-08-02 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bsn_card", "0002_details_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="details",
            name="com_name",
            field=models.CharField(default="", max_length=100),
        ),
    ]
