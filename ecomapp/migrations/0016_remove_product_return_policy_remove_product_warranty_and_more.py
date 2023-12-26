# Generated by Django 4.2.6 on 2023-12-26 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0015_rename_size10_5_productsize_size_10_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='return_policy',
        ),
        migrations.RemoveField(
            model_name='product',
            name='warranty',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]