# Generated by Django 4.0.6 on 2022-11-08 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('softLib', '0005_alter_book_added_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='Added_by',
            new_name='Addby',
        ),
    ]
