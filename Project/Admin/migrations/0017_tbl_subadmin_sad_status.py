# Generated by Django 4.2 on 2023-05-25 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0016_remove_tbl_subadmin_sad_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_subadmin',
            name='sad_status',
            field=models.CharField(default='1', max_length=1),
        ),
    ]
