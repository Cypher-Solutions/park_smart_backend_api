# Generated by Django 5.0.7 on 2024-07-14 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psba_app', '0002_alter_parkedinfo_totalparkingtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingspace',
            name='address',
            field=models.CharField(max_length=255),
        ),
    ]
