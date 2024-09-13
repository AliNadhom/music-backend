from django.contrib import admin
from .models import Artist, Album, Song

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist')

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'album')

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
