# Generated by Django 4.2.6 on 2023-12-26 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0013_alter_wishlist_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size6', models.BooleanField(default=True)),
                ('size6_5', models.BooleanField(default=True)),
                ('size7', models.BooleanField(default=True)),
                ('size7_5', models.BooleanField(default=True)),
                ('size8', models.BooleanField(default=True)),
                ('size8_5', models.BooleanField(default=True)),
                ('size9', models.BooleanField(default=True)),
                ('size9_5', models.BooleanField(default=True)),
                ('size10', models.BooleanField(default=True)),
                ('size10_5', models.BooleanField(default=True)),
                ('size11', models.BooleanField(default=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.product')),
            ],
        ),
    ]
