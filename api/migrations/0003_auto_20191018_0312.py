# Generated by Django 2.2.5 on 2019-10-18 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190915_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.TextField(blank=True),
        ),
    ]
