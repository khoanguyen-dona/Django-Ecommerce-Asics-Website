# Generated by Django 4.2.6 on 2024-01-08 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0025_productline_product_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='line',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
