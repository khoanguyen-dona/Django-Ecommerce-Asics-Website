# Generated by Django 4.2.6 on 2023-12-07 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_alter_cart_total_alter_cartproduct_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecomapp.customer'),
        ),
    ]
