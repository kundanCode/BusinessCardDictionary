# Generated by Django 4.2.3 on 2023-08-03 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bsn_card", "0003_details_com_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="details",
            name="comment",
            field=models.CharField(default="", max_length=100),
        ),
    ]
