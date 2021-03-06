# Generated by Django 2.2.5 on 2019-10-19 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_request_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sponsor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Sponsor'),
        ),
    ]
