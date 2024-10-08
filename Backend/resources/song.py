from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from model import db, Song, Artist, Album, PlaylistContent, Rate, roles_required
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os
from app import app
from cache import cache


class SongResource(Resource):
    @jwt_required()
    @cache.cached(timeout=300, query_string=True)
    def get(self, id):
        song_id = id
        if song_id == 0:
            songs = Song.query.all()
            return [song.serialize() for song in songs]
        song = Song.query.get(song_id)
        song.pcount+=1
        db.session.commit()
        if not song:
            return {"message": "Song not found"}, 404
        return song.serialize()

    @jwt_required()
    @roles_required(["creator","admin"])
    def post(self, id):
        cache.clear()
        # Check if the request contains the 'songfile' field
        print('song uploading')
        if "songfile" not in request.files:
            return {"message": "No file uploaded"}, 400

        songfile = request.files["songfile"]
        # Check if a file is selected
        if songfile.filename == "":
            return {"message": "No file selected"}, 400

        # Save the file
        if songfile:
            filename = secure_filename(songfile.filename)
            songfile.save("static/music/" + filename)
            song_path = "static/music/" + filename
        else:
            return {"message": "No file uploaded"}, 400

        # Retrieve other form fields
        songname = request.form.get("songname")
        artistnames = request.form.get("artistname")
        genre = request.form.get("genre")
        lyrics = request.form.get("lyrics")
        album = request.form.get("album")
        new_album_name = request.form.get("new_album_name")

        # Check if the songname already exists
        s = Song.query.filter_by(song_name=songname).all()
        if s:
            return {"message": "Songname already exists"}, 400

        user_id = int(id)
        # Create the song object
        song = Song(
            song_name=songname,
            song_path=song_path,
            song_lyrics=lyrics,
            song_genre=genre,
            rating=0,
            pcount=0,
            user_id=user_id,
        )
        db.session.add(song)

        # Handle artist names
        if artistnames!="" and artistnames!=" ":
            artist_names = [name.strip() for name in artistnames.split(",")]
            for artist_name in artist_names:
                artist = Artist.query.filter(
                    func.lower(Artist.artist_name) == func.lower(artist_name)
                ).first()
                if not artist:
                    artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                    db.session.add(artist)
                song.artists.append(artist)
                artist.songs.append(song)

        # Handle album
        if album != "none":
            if album == "new":
                if new_album_name:
                    n_album = Album(
                        album_name=new_album_name, rcount=0, user_id=user_id
                    )
                    # n_album.songs.append(song)
                    song.albums.append(n_album)
                else:
                    return {
                        "message": "New album name is required for creating a new album"
                    }, 400
            else:
                album_obj = Album.query.filter_by(album_name=album).first()
                if album_obj:
                    song.albums.append(album_obj)

        db.session.commit()
        return {"message": "Successful"}, 200

    @jwt_required()
    @roles_required(["creator","admin"])
    def delete(self, id):
        cache.clear()
        song_id = id
        song = Song.query.get(song_id)
        if song:
            # Delete related data manually according to model
            data = Rate.query.filter_by(songid=song_id).all()
            if data:
                for i in data:
                    db.session.delete(i)

            data2 = PlaylistContent.query.filter_by(song_id=song_id).all()
            if data2:
                for i in data2:
                    db.session.delete(i)

            for album in song.albums:
                album.songs.remove(song)
            for artist in song.artists:
                artist.songs.remove(song)

            # Delete the song file
            if os.path.exists(os.path.join(app.root_path, song.song_path)):
                os.remove(os.path.join(app.root_path, song.song_path))
            else:
                print("File does not exist at", os.path.join(app.root_path, song.song_path))


            db.session.delete(song)
            db.session.commit()
            return {"message": "Song deleted successfully"}, 200

        return {"message": "something went wrong"}

    @jwt_required()
    @roles_required(["creator","admin"])
    def patch(self, user_id, song_id):
        cache.clear()
        song = Song.query.get(song_id)
        if song:
            # Update song details
            song.song_name = request.json.get("songname")
            song.song_genre = request.json.get("genre")
            song.song_lyrics = request.json.get("lyrics")

            # Update artists
            artist_names = [
                name.strip() for name in request.json.get("artistname").split(",")
            ]
            song.artists.clear()  # Clear existing artists
            if artist_names!="" and artist_names!=" ":
                for artist_name in artist_names:
                    artist = Artist.query.filter(
                        func.lower(Artist.artist_name) == func.lower(artist_name)
                    ).first()
                    if not artist:
                        artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                        db.session.add(artist)
                    song.artists.append(artist)
                    # artist.songs.append(song)

            # Update album
            album_choice = request.json.get("album")
            if album_choice == "new":
                a_name = request.json.get("new_album_name")
                n_album = Album(album_name=a_name, rcount=0, user_id=user_id)
                n_album.songs.append(song)
                song.albums.append(n_album)
            elif album_choice == "none":
                song.albums = []
            elif album_choice == "nochange":
                pass
            else:
                album = Album.query.filter_by(album_name=album_choice).one()
                song.albums.append(album)

            db.session.commit()
            return {"message": "Song updated successfully"}, 200

        return {"message": "Song not found"}, 404

@jwt_required()
@cache.cached(timeout=300, query_string=True)
def genreSongs(genre):
    songs = Song.query.filter_by(song_genre=str(genre)).all()
    if songs:
        return [song.serialize() for song in songs]
    else:
        return {"message": "No song in this Genre"}, 404

@jwt_required()
@roles_required(["creator","admin"])
def songsbyuser(user_id):
    if int(user_id)==0:
        abort(404)
    songs=Song.query.filter_by(user_id=int(user_id)).all()
    if songs:
        return [song.serialize() for song in songs], 200
    else:
        return {"message":"No songs by user"}, 404