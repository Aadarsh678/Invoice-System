# Generated by Django 5.0.6 on 2024-05-20 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_alter_bill_invoice_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='product',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='quantity',
        ),
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.bill')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.product')),
            ],
        ),
    ]
