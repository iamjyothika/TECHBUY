# Generated by Django 5.0.2 on 2024-03-07 08:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDataModel',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=50)),
                ('user_phone', models.CharField(max_length=15)),
                ('user_email', models.CharField(max_length=100)),
                ('user_create_date', models.DateTimeField(auto_now_add=True)),
                ('user_status', models.CharField(default='active', max_length=7)),
            ],
            options={
                'db_table': 'user_data_model',
            },
        ),
        migrations.CreateModel(
            name='UserAddressDataModel',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('house_address', models.CharField(max_length=100)),
                ('city_address', models.TextField(max_length=50)),
                ('state_address', models.TextField(max_length=50)),
                ('pincode_address', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userdatamodel')),
            ],
            options={
                'db_table': 'user_address_model',
            },
        ),
        migrations.CreateModel(
            name='ReviewDataModel',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_review', models.CharField(max_length=255)),
                ('user_rating', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerapp.productmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userdatamodel')),
            ],
            options={
                'db_table': 'review_model',
            },
        ),
        migrations.CreateModel(
            name='OrderDetailsModel',
            fields=[
                ('user_order_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_order_quantity', models.IntegerField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('billing_ref_no', models.CharField(max_length=80)),
                ('status', models.TextField(max_length=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerapp.productmodel')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.useraddressdatamodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userdatamodel')),
            ],
            options={
                'db_table': 'order_model',
            },
        ),
        migrations.CreateModel(
            name='CartDataModel',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('cart_quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerapp.productmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userdatamodel')),
            ],
            options={
                'db_table': 'cart_model',
            },
        ),
        migrations.CreateModel(
            name='WishlistModel',
            fields=[
                ('wishlist_id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerapp.productmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userdatamodel')),
            ],
            options={
                'db_table': 'wishlist_model',
            },
        ),
    ]
