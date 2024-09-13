import graphene
from graphene_django import DjangoObjectType
from .models import Artist, Album, Song

class ArtistType(DjangoObjectType):
    class Meta:
        model = Artist

class AlbumType(DjangoObjectType):
    class Meta:
        model = Album
    artist = graphene.Field(ArtistType)

class SongType(DjangoObjectType):
    class Meta:
        model = Song
    artist = graphene.Field(ArtistType)

    def resolve_artist(self, info):
        return self.album.artist

class Query(graphene.ObjectType):
    all_artists = graphene.List(ArtistType)
    all_albums = graphene.List(AlbumType)
    all_songs = graphene.List(SongType)

    def resolve_all_artists(root, info):
        return Artist.objects.all()

    def resolve_all_albums(root, info):
        return Album.objects.all()

    def resolve_all_songs(root, info):
        return Song.objects.all()

class CreateArtistWithAlbumAndSongs(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        albumTitle = graphene.String(required=True)
        songs = graphene.List(graphene.String, required=True)

    artist = graphene.Field(ArtistType)

    def mutate(self, info, name, albumTitle, songs):
        artist = Artist(name=name)
        artist.save()

        album = Album(title=albumTitle, artist=artist)
        album.save()

        for song_title in songs:
            Song(title=song_title, album=album).save()

        return CreateArtistWithAlbumAndSongs(artist=artist)

class DeleteArtist(graphene.Mutation):
    class Arguments:
        artist_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, artist_id):
        try:
            artist = Artist.objects.get(pk=artist_id)
            artist.delete()
            return DeleteArtist(success=True)
        except Artist.DoesNotExist:
            return DeleteArtist(success=False)
        
class UpdateArtist(graphene.Mutation):
    class Arguments:
        artist_id = graphene.ID(required=True)
        new_name = graphene.String(required=True)

    artist = graphene.Field(ArtistType)

    def mutate(self, info, artist_id, new_name):
        try:
            artist = Artist.objects.get(pk=artist_id)
            artist.name = new_name
            artist.save()
            return UpdateArtist(artist=artist)
        except Artist.DoesNotExist:
            return UpdateArtist(artist=None)


class UpdateAlbum(graphene.Mutation):
    class Arguments:
        album_id = graphene.ID(required=True)
        new_title = graphene.String(required=True)

    album = graphene.Field(AlbumType)

    def mutate(self, info, album_id, new_title):
        try:
            album = Album.objects.get(pk=album_id)
            album.title = new_title
            album.save()
            return UpdateAlbum(album=album)
        except Album.DoesNotExist:
            return UpdateAlbum(album=None)

class Mutation(graphene.ObjectType):
    add_artist_with_album_and_songs = CreateArtistWithAlbumAndSongs.Field()
    delete_artist = DeleteArtist.Field()
    update_artist = UpdateArtist.Field()
    update_album = UpdateAlbum.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
