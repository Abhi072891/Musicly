from flask_restful import Resource, marshal_with, fields, reqparse
from flask import request, abort
from sqlalchemy import func
from model import db, Song, Artist

# Define the fields for marshaling artist data
artist_fields = {
    'artist_id': fields.Integer,
    'artist_name': fields.String,
    'scount': fields.Integer,
    'user_id': fields.Integer
}

class ArtistResource(Resource):
    # @marshal_with(artist_fields)
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