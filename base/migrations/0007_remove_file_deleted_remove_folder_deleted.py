# Generated by Django 4.1.1 on 2022-09-24 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_file_deleted_folder_deleted_alter_file_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='folder',
            name='deleted',
        ),
    ]
