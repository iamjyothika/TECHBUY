# Generated by Django 5.0.2 on 2024-03-15 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerapp', '0012_alter_pcspecificationmodel_spec_resolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcspecificationmodel',
            name='spec_gpu',
            field=models.CharField(max_length=20),
        ),
    ]
