# Generated by Django 4.0.5 on 2022-06-11 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csgh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deliveryId', models.CharField(max_length=20)),
                ('shipToName', models.CharField(max_length=100)),
                ('product_id', models.CharField(max_length=10)),
                ('product', models.CharField(max_length=225)),
                ('qty', models.IntegerField()),
                ('valid_to_date', models.DateField(verbose_name='valid date')),
                ('created_date', models.DateField(verbose_name='date processed')),
            ],
            options={
                'verbose_name_plural': 'Supply Data',
                'ordering': ['-created_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='retailprice',
            options={'ordering': ['-price'], 'verbose_name_plural': 'Retail Prices'},
        ),
        migrations.AlterModelOptions(
            name='salesquotelogs',
            options={'ordering': ['-created_date'], 'verbose_name_plural': 'Sales Quotes'},
        ),
        migrations.AlterModelOptions(
            name='whprice',
            options={'ordering': ['-price'], 'verbose_name_plural': 'WH Prices'},
        ),
    ]