# Generated by Django 2.2.2 on 2019-06-09 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_request_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='location',
            field=models.CharField(default='Now', max_length=30),
            preserve_default=False,
        ),
    ]
