from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify
from model import db, Playlist, PlaylistContent, Song, roles_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache import cache

# Define fields for marshalling playlist data
playlist_fields = {
    'playlist_id': fields.Integer,
    'user_id': fields.Integer,
    'playlist_name': fields.String
}

class PlaylistResource(Resource):
    @jwt_required()
    @marshal_with(playlist_fields)
    def get(self, user_id, pl_id):
        if pl_id==0:
            playlists = Playlist.query.filter_by(user_id=user_id).all()
        else:
            playlists=Playlist.query.get(pl_id)
        return playlists

    @marshal_with(playlist_fields)
    @jwt_required()
    def post(self, id):
        user_id=id
        parser = reqparse.RequestParser()
        parser.add_argument('playlist_id')
        parser.add_argument('song_ids', type=int, action='append')
        parser.add_argument('new_playlist_name', type=str)
        args = parser.parse_args()

        pl_id = args['playlist_id']
        song_ids = args['song_ids']
        new_playlist_name = args['new_playlist_name']

        if pl_id == 'new':
            new_playlist = Playlist(user_id=user_id, playlist_name=new_playlist_name)
            db.session.add(new_playlist)
            db.session.commit()
            pl_id = new_playlist.playlist_id

        if song_ids:
            for song_id in song_ids:
                playlist_song = PlaylistContent(playlist_id=int(pl_id), song_id=song_id)
                db.session.add(playlist_song)
            db.session.commit()

        return Playlist.query.get(pl_id), 201

    @marshal_with(playlist_fields)
    @jwt_required()
    def patch(self, id):
        pl_id=id
        parser = reqparse.RequestParser()
        parser.add_argument('playlist_name', type=str)
        args = parser.parse_args()

        playlist = Playlist.query.get(pl_id)
        if playlist:
            playlist.playlist_name = args['playlist_name'] or playlist.playlist_name
            db.session.commit()
            return playlist
        else:
            return {'message': 'Playlist not found'}, 404

    @jwt_required()
    def delete(self, id):
        pl_id=id
        playlist = Playlist.query.get(pl_id)
        if playlist:
            playlist_content = PlaylistContent.query.filter_by(playlist_id=pl_id).all()
            for content in playlist_content:
                db.session.delete(content)
            db.session.delete(playlist)
            db.session.commit()
            return {'message': 'Playlist deleted successfully'}, 200
        else:
            return {'message': 'Playlist not found'}, 404


        #---------------Custom functions------------#
@jwt_required()
def addsongtopl(pl_id,song_id,):
    data=PlaylistContent.query.filter_by(song_id=song_id, playlist_id=pl_id).first()
    if not data:
        playlist_song = PlaylistContent(playlist_id=pl_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
    return {'message': 'Song added to playlist'}

@jwt_required()
def removesongfrompl(pl_id,song_id):
    data=PlaylistContent.query.filter_by(song_id=song_id, playlist_id=pl_id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
    return {'message': 'Song removed from playlist'}

@jwt_required()
def showpl(pl_id):
    plsongs=[]
    plcontent=PlaylistContent.query.filter_by(playlist_id=pl_id).all()
    for i in plcontent:
        s=Song.query.get(i.song_id)
        temp={
            "id": s.song_id,
            "name": s.song_name,
            "path": s.song_path
        }
        plsongs.append(temp)
    return plsongs
    


    