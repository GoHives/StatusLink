# Generated by Django 3.2 on 2022-10-31 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0002_auto_20221029_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processsteps',
            old_name='process_steps',
            new_name='process_status',
        ),
    ]