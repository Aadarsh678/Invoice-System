# Generated by Django 5.0.6 on 2024-05-22 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0014_alter_billitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.product'),
        ),
    ]