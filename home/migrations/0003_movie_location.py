# Generated by Django 3.0.2 on 2020-02-05 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Location'),
        ),
    ]
