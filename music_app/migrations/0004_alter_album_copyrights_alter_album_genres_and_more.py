# Generated by Django 4.1.7 on 2023-03-03 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0003_alter_album_is_full_record_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='copyrights',
            field=models.ManyToManyField(null=True, related_name='albums', to='music_app.copyrightalbum'),
        ),
        migrations.AlterField(
            model_name='album',
            name='genres',
            field=models.ManyToManyField(null=True, related_name='albums', to='music_app.genre'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='genres',
            field=models.ManyToManyField(null=True, related_name='artists', to='music_app.genre'),
        ),
    ]
