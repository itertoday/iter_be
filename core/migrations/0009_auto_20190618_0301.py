# Generated by Django 2.2.2 on 2019-06-18 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190616_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('shipped', 'shipped'), ('cancelled', 'cancelled'), ('accepted', 'accepted'), ('in transit', 'in transit')], max_length=20),
        ),
    ]
