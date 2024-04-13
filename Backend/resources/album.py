from flask_restful import Resource, marshal_with, fields, reqparse
from flask import request, abort
from sqlalchemy import func
from model import db, Album, Song, Artist
from cache import cache


class AlbumResource(Resource):
    @jwt_required()
    @cache.cached(timeout=300, query_string=True)
    def get(self, id):
        album_id=id
        if album_id==0:
            albums=Album.query.all()
            return [album.serialize() for album in albums] ,200
        album = Album.query.get(album_id)
        if album:
            temp = int(album.rcount)
            temp = temp + 1
            album.rcount = temp
            db.session.commit()
            return album.serialize(), 200
        else:
            return {'message': 'Album not found'}, 404
        
    @jwt_required()
    @roles_required(["creator","admin"])
    def post(self, id):
        cache.clear()
        user_id=id
        parser = reqparse.RequestParser()
        parser.add_argument('album_name', type=str, required=True)
        parser.add_argument('song_ids', type=int, action='append', required=False)
        parser.add_argument('artist_names', type=str, action='append', required=False)
        args = parser.parse_args()

        album_name = args['album_name']
        song_ids = args['song_ids'] or []
        artist_names = args['artist_names'] or []

        # Check if album name already exists
        existing_album = Album.query.filter_by(album_name=album_name).first()
        if existing_album:
            return {'message': 'Album name already exists'}, 409

        # Create a new album
        album = Album(album_name=album_name, user_id=user_id, rcount=1)
        db.session.add(album)

        # Add songs to the album
        if song_ids:
            songs = Song.query.filter(Song.song_id.in_(song_ids)).all()
            album.songs.extend(songs)

        # Add artists to the album
        if artist_names:
            artists = []
            for artist_name in artist_names:
                artist = Artist.query.filter(func.lower(Artist.artist_name) == func.lower(artist_name)).first()
                if not artist:
                    artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                    db.session.add(artist)
                artists.append(artist)
            album.artists.extend(artists)

        db.session.commit()
        return album.serialize(), 201

    @jwt_required()
    @roles_required(["creator","admin"])
    def patch(self, album_id, user_id):
        cache.clear()
        album = Album.query.get(album_id)
        if album:
            # Update album details if provided
            if 'album_name' in request.json:
                album.album_name = request.json['album_name']

            # Add songs to the album if provided
            song_ids = request.json.get('song_ids', [])
            if song_ids:
                album.songs = Song.query.filter(Song.song_id.in_(song_ids)).all()
            else:
                album.songs=[]

            # Add artists to the album if provided
            artist_names = request.json.get('artist_names', [])
            if artist_names:
                album.artists=[]
                for artist_name in artist_names:
                    artist = Artist.query.filter(func.lower(Artist.artist_name) == func.lower(artist_name)).first()
                    if not artist:
                        artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                        db.session.add(artist)
                    album.artists.append(artist)
            db.session.commit()
            return album.serialize()
        else:
            return {'message': 'Album not found'}, 404

    @jwt_required()
    @roles_required(["creator","admin"])
    def delete(self, id):
        cache.clear()
        album_id=id
        album = Album.query.get(album_id)
        if album:
             # Remove songs associated with the album
            for song in album.songs:
                album.songs.remove(song)
            # Remove artists associated with the album
            for artist in album.artists:
                album.artists.remove(artist)

            db.session.delete(album)
            db.session.commit()
            return {'message': 'Album deleted successfully'}, 200
        else:
            return {'message': 'Album not found'}, 404
        

@jwt_required()
@roles_required(["creator","admin"])
def removesongfromalbum(album_id,song_id):
    cache.clear()
    song=Song.query.get(song_id)
    album=Album.query.get(album_id)
    song.albums.remove(album)
    db.session.commit()
    return {'message':'Song removed from album'}

@jwt_required()
@roles_required(["creator","admin"])
def addsongtoalbum(album_id,song_id):
    cache.clear()
    song = Song.query.get(song_id)
    album = Album.query.get(album_id)
    if song and album:
        if not song in album.songs:
            album.songs.append(song)
            db.session.commit()
            return f'Song "{song.song_name}" added to album "{album.album_name}" successfully'
    return abort(400,{'message':'no update'})

@jwt_required()
@roles_required(["creator","admin"])
def albumsbyuser(user_id):
    if int(user_id)==0:
        abort(404)
    albums=Album.query.filter_by(user_id=int(user_id)).all()
    if albums:
        return [album.serialize() for album in albums] ,200
    else:
        return {"message":"no album by user"}, 404
