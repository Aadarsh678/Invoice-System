# Generated by Django 5.0.6 on 2024-05-16 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_bill_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='deleted',
        ),
    ]
