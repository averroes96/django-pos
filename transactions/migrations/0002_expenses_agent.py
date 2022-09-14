# Generated by Django 3.2.15 on 2022-09-14 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_init_agents_permissions'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='agents.agent'),
        ),
    ]