# Generated by Django 4.2 on 2023-05-31 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0001_initial'),
        ('Guest', '0007_tbl_market_reg_mar_status'),
        ('Farmer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_m_booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_status', models.CharField(default='0', max_length=1)),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.tbl_farmer_reg')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_m_cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mquantity', models.CharField(default='1', max_length=1)),
                ('bookingid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Farmer.tbl_m_booking')),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Market.tbl_market_product')),
            ],
        ),
    ]