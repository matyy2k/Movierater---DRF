# Generated by Django 4.0.2 on 2022-02-16 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_film_imdb_rating_film_release_date_film_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='year',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
    ]
