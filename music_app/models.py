from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MinLengthValidator


class ExternalID(models.Model):
    name = models.CharField('External ID name', max_length=30, null=False, unique=True)
    value = models.CharField('External ID value', max_length=30, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=False)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f'{self.name} - {self.value}'


class Market(models.Model):
    code = models.CharField('Code Market', max_length=2, validators=[
        MaxLengthValidator(2),
        MinLengthValidator(2),
    ], null=False, unique=True)

    def __str__(self):
        return self.code


class Genre(models.Model):
    name = models.CharField('Genre name', max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField("Group name", max_length=100, null=False)
    artist_image_url = models.URLField('Artist image URL')
    spotify_id = models.CharField('Spotify ID', max_length=22, validators=[
        MaxLengthValidator(22),
        MinLengthValidator(22),
    ], unique=True, null=False, db_index=True)
    spotify_uri = models.CharField('Spotify URI', max_length=50, unique=True, null=False)
    genres = models.ManyToManyField('Genre', related_name='artists')

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField('Track name', max_length=100, null=False)
    track_number_of_album = models.PositiveSmallIntegerField('Track number of album')
    duration_ms = models.PositiveIntegerField('Track duration (ms)')
    spotify_id = models.CharField('Spotify ID', max_length=22, validators=[
        MaxLengthValidator(22),
        MinLengthValidator(22),
    ], unique=True, null=False, db_index=True)
    spotify_uri = models.CharField('Spotify URI', max_length=50, unique=True)
    is_explicit = models.BooleanField('Explicit')
    album = models.ForeignKey('Album', related_name='tracks', on_delete=models.CASCADE, null=False)
    artists = models.ManyToManyField('Artist', related_name='tracks')
    available_markets = models.ManyToManyField('Market', related_name='tracks')
    external_ids = GenericRelation(ExternalID)

    def __str__(self):
        return self.name


class AlbumType(models.Model):
    name = models.CharField('Album type name', max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name


class CopyrightAlbumType(models.Model):
    name = models.CharField('Copyright type name', max_length=20, null=False, unique=True)

    def __str__(self):
        return self.name


class CopyrightAlbum(models.Model):
    text = models.CharField('Copyright text', max_length=100, null=False, unique=True)
    copyright_type = models.ForeignKey('CopyrightAlbumType', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.text[:20]}...'


class Album(models.Model):
    name = models.CharField('Album name', max_length=100, null=False)
    spotify_id = models.CharField('Spotify ID', max_length=22, validators=[
        MaxLengthValidator(22),
        MinLengthValidator(22),
    ], unique=True, null=False, db_index=True)
    spotify_uri = models.CharField('Spotify URI', max_length=50, null=False, unique=True)
    release_date = models.DateField('Release date')
    album_image_url = models.URLField('Album image URL')
    album_type = models.ForeignKey('AlbumType', on_delete=models.CASCADE)
    copyrights = models.ManyToManyField('CopyrightAlbum', related_name='albums')
    artists = models.ManyToManyField('Artist', related_name='albums')
    genres = models.ManyToManyField('Genre',  related_name='albums')
    available_markets = models.ManyToManyField('Market', related_name='albums')
    external_ids = GenericRelation(ExternalID)

    def __str__(self):
        return self.name
