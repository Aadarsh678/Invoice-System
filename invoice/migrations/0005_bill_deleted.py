# Generated by Django 5.0.6 on 2024-05-16 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_alter_bill_invoice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
