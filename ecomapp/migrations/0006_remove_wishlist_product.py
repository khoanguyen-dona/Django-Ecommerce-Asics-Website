# Generated by Django 4.2.6 on 2023-12-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0005_alter_wishlist_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
    ]