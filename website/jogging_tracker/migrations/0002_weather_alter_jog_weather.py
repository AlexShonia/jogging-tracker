# Generated by Django 5.0.6 on 2024-07-11 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogging_tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.IntegerField()),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='jog',
            name='weather',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='jogging_tracker.weather'),
        ),
    ]
