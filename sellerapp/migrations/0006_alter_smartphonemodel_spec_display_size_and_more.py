# Generated by Django 5.0.2 on 2024-03-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0005_alter_pcspecificationmodel_spec_processor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphonemodel',
            name='spec_display_size',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='smartphonemodel',
            name='spec_resolution',
            field=models.CharField(max_length=30),
        ),
    ]
