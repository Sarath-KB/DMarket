# Generated by Django 4.2.3 on 2023-07-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0010_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_cus_reg',
            name='cus_contact',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='tbl_farmer_reg',
            name='far_contact',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='tbl_market_reg',
            name='mar_contact',
            field=models.CharField(max_length=12),
        ),
    ]