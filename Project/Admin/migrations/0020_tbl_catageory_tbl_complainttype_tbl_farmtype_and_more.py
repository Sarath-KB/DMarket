# Generated by Django 4.2.3 on 2023-07-08 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0019_delete_tbl_complainttype_delete_tbl_farmtype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_catageory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=50)),
                ('cat_status', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_complainttype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_farmtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_subcat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcat_name', models.CharField(max_length=50)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_catageory')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_subadmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sad_name', models.CharField(max_length=50)),
                ('sad_contact', models.CharField(max_length=10)),
                ('sad_email', models.CharField(max_length=50)),
                ('sad_address', models.CharField(max_length=100)),
                ('sad_photo', models.FileField(upload_to='SubadminPhoto/')),
                ('sad_pass', models.CharField(max_length=50)),
                ('sad_doj', models.DateField(auto_now_add=True)),
                ('sad_status', models.CharField(default='1', max_length=1)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_district')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_local_place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_place_name', models.CharField(max_length=50)),
                ('pla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_place')),
            ],
        ),
    ]
