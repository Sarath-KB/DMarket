# Generated by Django 4.2.3 on 2023-07-08 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0014_remove_tbl_market_product_market_and_more'),
        ('Customer', '0017_remove_tbl_farmer_booking_user_and_more'),
        ('Farmer', '0012_remove_tbl_m_booking_farmer_and_more'),
        ('Guest', '0008_tbl_feedback_tbl_complaint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_cus_reg',
            name='cus_locplace',
        ),
        migrations.RemoveField(
            model_name='tbl_farmer_reg',
            name='farmer_type',
        ),
        migrations.RemoveField(
            model_name='tbl_farmer_reg',
            name='locplace',
        ),
        migrations.RemoveField(
            model_name='tbl_feedback',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='tbl_feedback',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='tbl_feedback',
            name='market',
        ),
        migrations.RemoveField(
            model_name='tbl_feedback',
            name='subadmin',
        ),
        migrations.RemoveField(
            model_name='tbl_market_reg',
            name='place',
        ),
        migrations.DeleteModel(
            name='tbl_complaint',
        ),
        migrations.DeleteModel(
            name='tbl_cus_reg',
        ),
        migrations.DeleteModel(
            name='tbl_farmer_reg',
        ),
        migrations.DeleteModel(
            name='tbl_feedback',
        ),
        migrations.DeleteModel(
            name='tbl_market_reg',
        ),
    ]
