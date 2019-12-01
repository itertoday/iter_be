# Generated by Django 2.2.5 on 2019-11-24 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20191027_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(help_text='Calle', max_length=100, null=True)),
                ('comuna', models.CharField(help_text='Comuna', max_length=100, null=True)),
                ('department', models.CharField(help_text='Departamento', max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=13, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('Nuevo', 'New'), ('Recarga', 'Reload')], max_length=100, null=True),
        ),
    ]