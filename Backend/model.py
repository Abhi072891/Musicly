from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import DateTime
from sqlalchemy.sql import func


db = SQLAlchemy()


# Create association tables for many-to-many relationships
song_album_association = db.Table('song_album_association',
    db.Column('song_id', db.Integer, db.ForeignKey('Songs.song_id')),
    db.Column('album_id', db.Integer, db.ForeignKey('Albums.album_id'))
)

song_artist_association = db.Table('song_artist_association',
    db.Column('song_id', db.Integer, db.ForeignKey('Songs.song_id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artists.artist_id'))
)

album_artist_association = db.Table('album_artist_association',
    db.Column('album_id', db.Integer, db.ForeignKey('Albums.album_id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artists.artist_id'))
)

class Song(db.Model):
    __tablename__ = 'Songs'
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    song_genre = db.Column(db.String(100))
    song_lyrics = db.Column(db.String())
    song_path = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    pcount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # Define the many-to-many relationship with albums
    albums = db.relationship('Album', secondary=song_album_association, backref=db.backref('songs', lazy='dynamic'))

    # Define the many-to-many relationship with artists
    artists = db.relationship('Artist', secondary=song_artist_association, backref=db.backref('songs', lazy='dynamic'))

    def __repr__(self):
        return f"<Song(song_name='{self.song_name}')>"

    def serialize(self):
        return {
            'song_id': self.song_id,
            'song_name': self.song_name,
            'song_genre': self.song_genre,
            'song_lyrics': self.song_lyrics,
            'song_path': self.song_path,
            'rating': self.rating,
            'pcount': self.pcount,
            'albums': [{'id':album.album_id,'name':album.album_name} for album in self.albums],
            'artists': [{'id':artist.artist_id,'name':artist.artist_name} for artist in self.artists]
        }
    
class Rate(db.Model):
    rate_id = db.Column(db.Integer, primary_key=True)
    songid = db.Column(db.Integer, db.ForeignKey('Songs.song_id'))
    userid = db.Column(db.Integer, db.ForeignKey('User.id'))
    ratinggiven = db.Column(db.Integer)

class Artist(db.Model):
    __tablename__ = 'Artists'
    user_id = db.Column(db.Integer)
    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    scount = db.Column(db.Integer)

    # Define the many-to-many relationship with albums
    albums = db.relationship('Album', secondary=album_artist_association, backref=db.backref('artists', lazy='dynamic'))

    def __repr__(self):
        return f"<Artist(artist_name='{self.artist_name}')>"

    def serialize(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist_name,
            'scount': self.scount,
            'albums': [{'id':album.album_id,'name':album.album_name} for album in self.albums],
            'songs':[{'id':song.song_id,'name':song.song_name,'path':song.song_path} for song in self.songs]
        }
    
class Album(db.Model):
    __tablename__ = 'Albums'
    album_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album_name = db.Column(db.String(100), nullable=False, index=True)
    rcount= db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f"<Album(album_name='{self.album_name}')>"

    def serialize(self):
        return {
            'album_id': self.album_id,
            'album_name': self.album_name,
            'rcount': self.rcount,
            'artists':[{'id':artist.artist_id,'name':artist.artist_name} for artist in self.artists],
            # 'songs':[song.song_id for song in self.songs]
            'songs':[{'id':song.song_id,'name':song.song_name,'path':song.song_path} for song in self.songs]
        }
    

class Playlist(db.Model):
    __tablename__ = 'Playlists'
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    playlist_name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

class PlaylistContent(db.Model):
    __tablename__ = 'PlaylistContents'
    pcid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('Playlists.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.song_id'))


# Define the Role model
class Role(db.Model):
    __tablename__='Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

# Define the association table for the many-to-many relationship between users and roles
user_role_association = db.Table('user_role_association',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
)

class User(db.Model):
    __tablename__='User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String())
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    roles = db.relationship('Role', secondary=user_role_association, backref=db.backref('users', lazy='dynamic'))
    status = db.Column(db.String(), default='0')
    login_at = db.Column(db.DateTime, default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


def roles_required(roles):
    #roles : A list of roles to be approved
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                id = get_jwt_identity()

                if not id:
                    return {"message" : "Token is invalid"} , 403

                user = User.query.filter_by(id = id).first()
                if not user:
                    return {"message" : "User not found"} , 404
                for role in [role.name for role in user.roles]:
                    if role in roles:
                        return fn(*args, **kwargs)
                
                return {"message" : "Not authorised to access this page"} , 401
                

            except Exception as e:
                print("Error from roles required", e)
                return {"message" : "Internal Server Error"} , 500

        return wrapper
    return decorator
