# Generated by Django 2.2.5 on 2019-10-27 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_product_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Nuevo', 'New'), ('Recarga', 'Reload')], max_length=100),
        ),
    ]
