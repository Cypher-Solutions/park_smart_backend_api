# Generated by Django 5.0.7 on 2024-07-14 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('address', models.TextField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=1000000, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=10)),
                ('prepaid', models.BooleanField()),
                ('is_available', models.BooleanField(default=False)),
                ('space_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Motorist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParkedInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duriation', models.CharField(max_length=20)),
                ('entryTime', models.DateTimeField(auto_now_add=True)),
                ('exitTime', models.DateTimeField(auto_now=True)),
                ('totalParkingTime', models.DecimalField(decimal_places=2, max_digits=999999)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parked_motorist', to='psba_app.motorist')),
                ('parking_space', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parked_space_info', to='psba_app.parkingspace')),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_motorist', to='psba_app.motorist')),
                ('parking_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fav_space', to='psba_app.parkingspace')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_reg', models.CharField(max_length=8)),
                ('model', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motirist_vehicle', to='psba_app.motorist')),
            ],
        ),
    ]
