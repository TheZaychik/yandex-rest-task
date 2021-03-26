# Generated by Django 3.1.7 on 2021-03-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='completed_delivery',
        ),
        migrations.AddField(
            model_name='courier',
            name='delivery',
            field=models.JSONField(default=[], verbose_name='Delivery'),
        ),
    ]