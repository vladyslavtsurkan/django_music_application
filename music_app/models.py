from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    children = GenericRelation('self')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.content[:15]}...' if len(self.content) > 15 else f'{self.content}'


class ExternalID(models.Model):
    name = models.CharField(_('External ID name'), max_length=50, null=False)
    value = models.CharField(_('External ID value'), max_length=50, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=False)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f'{self.name} - {self.value}'


class Market(models.Model):
    code = models.CharField(_('Code Market'), max_length=2, validators=[
        MaxLengthValidator(2),
        MinLengthValidator(2),
    ], null=False, unique=True)

    def __str__(self):
        return self.code


class Genre(models.Model):
    name = models.CharField(_('Genre name'), max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(_("Group name"), max_length=300, null=False)
    artist_image_url = models.URLField(_('Artist image URL'), null=True)
    spotify_id = models.CharField('Spotify ID', max_length=22, validators=[
        MaxLengthValidator(22),
        MinLengthValidator(22),
    ], unique=True, null=False, db_index=True)
    spotify_uri = models.CharField('Spotify URI', max_length=50, unique=True, null=False)
    genres = models.ManyToManyField('Genre', related_name='artists')
    comments = GenericRelation(Comment, related_name='artist')
    is_full_record = models.BooleanField(_('Full record about artist'), default=False)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(_('Track name'), max_length=300, null=False)
    track_number_of_album = models.PositiveSmallIntegerField(_('Track number of album'))
    duration_ms = models.PositiveIntegerField(_('Track duration (ms)'))
    spotify_id = models.CharField('Spotify ID', max_length=22, validators=[
        MaxLengthValidator(22),
        MinLengthValidator(22),
    ], unique=True, null=False, db_index=True)
    spotify_uri = models.CharField('Spotify URI', max_length=50, unique=True)
    is_explicit = models.BooleanField(_('Explicit'))
    album = models.ForeignKey('Album', related_name='tracks', on_delete=models.CASCADE, null=True)
    artists = models.ManyToManyField('Artist', related_name='tracks')
    available_markets = models.ManyToManyField('Market', related_name='tracks')
    external_ids = GenericRelation(ExternalID)
    comments = GenericRelation(Comment, related_name='track')
    is_full_record = models.BooleanField(_('Full record about track'), default=False)

    def __str__(self):
        return self.name


class AlbumType(models.Model):
    name = models.CharField(_('Album type name'), max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name


class CopyrightAlbumType(models.Model):
    name = models.CharField(_('Copyright type name'), max_length=20, null=False, unique=True)

    def __str__(self):
        return self.name


class CopyrightAlbum(models.Model):
    text = models.CharField(_('Copyright text'), max_length=300, null=False)
    copyright_type = models.ForeignKey('CopyrightAlbumType', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.text[:20]}...'


class Album(models.Model):
    name = models.CharField(_('Album name'), max_length=300, null=False)
    spotify_id = models.CharField('Spotify ID', max_length=22, validators=[
        MaxLengthValidator(22),
        MinLengthValidator(22),
    ], unique=True, null=False, db_index=True)
    spotify_uri = models.CharField('Spotify URI', max_length=50, null=False, unique=True)
    release_date = models.DateField(_('Release date'))
    album_image_url = models.URLField(_('Album image URL'), null=True)
    album_type = models.ForeignKey('AlbumType', on_delete=models.CASCADE)
    copyrights = models.ManyToManyField('CopyrightAlbum', related_name='albums')
    artists = models.ManyToManyField('Artist', related_name='albums')
    genres = models.ManyToManyField('Genre',  related_name='albums')
    available_markets = models.ManyToManyField('Market', related_name='albums')
    external_ids = GenericRelation(ExternalID)
    comments = GenericRelation(Comment, related_name='album')
    is_full_record = models.BooleanField(_('Full record about album'), default=False)

    def __str__(self):
        return self.name
