# Generated by Django 5.0.6 on 2024-05-21 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_remove_bill_product_remove_bill_quantity_billitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]