# Generated by Django 2.2 on 2020-02-19 04:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20200219_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielocation',
            name='movie',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Movie'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='movie',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Movie'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
