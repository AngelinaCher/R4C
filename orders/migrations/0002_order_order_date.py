# Generated by Django 4.2.5 on 2023-09-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now=True),
        ),
    ]
