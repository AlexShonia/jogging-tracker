# Generated by Django 5.0.6 on 2024-06-23 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogging_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jog',
            name='weather',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('manager', 'Manager'), ('admin', 'Admin')], default='customer', max_length=255),
        ),
    ]