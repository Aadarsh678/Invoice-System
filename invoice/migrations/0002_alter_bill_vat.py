# Generated by Django 5.0.6 on 2024-05-15 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='vat',
            field=models.DecimalField(decimal_places=2, default=13, max_digits=10),
        ),
    ]