# Generated by Django 3.2.15 on 2022-09-16 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='margin',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='article',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='quantity_minimum',
            field=models.IntegerField(default=0),
        ),
    ]
