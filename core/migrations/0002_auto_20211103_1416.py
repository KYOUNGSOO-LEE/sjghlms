# Generated by Django 3.2.7 on 2021-11-03 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='flagged_by',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
    ]