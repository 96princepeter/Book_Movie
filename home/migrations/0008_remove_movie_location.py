# Generated by Django 3.0.2 on 2020-02-10 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200210_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='location',
        ),
    ]
