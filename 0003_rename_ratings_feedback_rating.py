# Generated by Django 4.2.7 on 2024-12-22 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Base_App', '0002_alter_items_image_alter_items_item_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='Ratings',
            new_name='Rating',
        ),
    ]
