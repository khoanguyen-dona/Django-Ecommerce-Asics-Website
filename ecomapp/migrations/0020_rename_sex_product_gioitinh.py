# Generated by Django 4.2.6 on 2024-01-07 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0019_product_sex_alter_product_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sex',
            new_name='gioitinh',
        ),
    ]
