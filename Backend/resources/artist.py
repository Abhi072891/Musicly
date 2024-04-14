from flask_restful import Resource, marshal_with, fields, reqparse
from flask import request, abort
from sqlalchemy import func
from model import db, Song, Artist, roles_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache import cache

class ArtistResource(Resource):
    @cache.cached(timeout=300, query_string=True)
    def get(self, id):
        artist_id=id
        if artist_id==0:
            artists=Artist.query.all()
            return [artist.serialize() for artist in artists] 
        artist = Artist.query.get(artist_id)
        if artist:
            artist.scount += 1
            db.session.commit()
            return artist.serialize()
        else:
            return {'message': 'artist not found'}, 404
        

    @jwt_required()
    @roles_required(["creator","admin"])
    def delete(self, id):
        artist_id=id
        artist = Artist.query.get(artist_id)
        if artist:
             # Remove songs associated with the artist
            for song in artist.songs:
                artist.songs.remove(song)
            # Remove albums associated with the artist
            for album in artist.albums:
                artist.albums.remove(album)

            db.session.delete(artist)
            db.session.commit()
            return {'message': 'artist deleted successfully'}, 200
        else:
            return {'message': 'artist not found'}, 404