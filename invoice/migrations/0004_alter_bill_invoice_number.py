# Generated by Django 5.0.6 on 2024-05-16 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_bill_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='invoice_number',
            field=models.CharField(default=0, max_length=100, unique=True),
        ),
    ]