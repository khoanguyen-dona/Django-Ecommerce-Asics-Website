# Generated by Django 4.2.6 on 2023-12-09 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0006_remove_wishlist_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
