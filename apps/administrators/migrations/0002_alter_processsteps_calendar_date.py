# Generated by Django 3.2 on 2022-11-03 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrators', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processsteps',
            name='calendar_date',
            field=models.DateField(blank=True, db_column='CalendarDate', null=True),
        ),
    ]
