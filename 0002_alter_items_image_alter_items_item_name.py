# Generated by Django 5.1.4 on 2024-12-20 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='Image',
            field=models.ImageField(upload_to='items/'),
        ),
        migrations.AlterField(
            model_name='items',
            name='Item_name',
            field=models.CharField(max_length=40),
        ),
    ]
