# Generated by Django 5.0.2 on 2024-06-01 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0023_productdiscount_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdiscount',
            name='seller_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sellerapp.sellerdatamodel'),
        ),
    ]
