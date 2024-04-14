from flask import Flask
from flask_restful import  Api
from model import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:5173",
            "supports_credentials": True,
            "Access-Control-Allow-Credentials": True,
        }
    },
)


# User registration and login endpoints
from resources.user import UserRegister, UserLogin, AdminLogin, adminstats, creatorwaiting, ProtectedResource, check_email_availability, check_username_availability, creatorapplication, creatorapprove, creatorreject, allcreators, blacklist_creator, whitelist_creator
api.add_resource(ProtectedResource, '/jwt/testing')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(AdminLogin, '/admin/login')
app.add_url_rule('/adminstats','adminstats',(adminstats),methods=["GET"])
app.add_url_rule('/creatorwaiting','creatorwaiting',(creatorwaiting),methods=["GET"])
app.add_url_rule('/blacklistcreator/<int:user_id>', 'blacklist_creator', blacklist_creator, methods=["GET"])
app.add_url_rule('/whitelistcreator/<int:user_id>', 'whitelist_creator', whitelist_creator, methods=["GET"])
app.add_url_rule('/allcreators', 'allcreators', allcreators, methods=["GET"])
app.add_url_rule('/check-email/<email>', "check_email_availability", (check_email_availability), methods=["GET"])
app.add_url_rule('/check-username/<username>', "check_username_availability", (check_username_availability), methods=["GET"])
app.add_url_rule('/creator-application/<int:user_id>', "creator_application", (creatorapplication), methods=["POST"])
app.add_url_rule('/creator-approve/<int:user_id>', "creator_approve", (creatorapprove), methods=["GET"])
app.add_url_rule('/creator-reject/<int:user_id>', "creator_reject", (creatorreject), methods=["GET"])


# Song endpoints
from resources.song import SongResource, genreSongs, songsbyuser
api.add_resource(SongResource, '/songs/<int:id>', 
                               '/songs/<int:user_id>/<int:song_id>')
app.add_url_rule('/genre/<genre>', "genreSongs",(genreSongs), methods=["GET"])
app.add_url_rule('/songsbyuser/<int:user_id>', "songsbyuser",(songsbyuser), methods=["GET"])

# Album endpoints
from resources.album import AlbumResource, removesongfromalbum, addsongtoalbum, albumsbyuser
api.add_resource(AlbumResource, '/albums/<int:id>', 
                                '/albums/<int:album_id>/<int:user_id>')
app.add_url_rule("/removesongfromalbum/<int:album_id>/<int:song_id>", "removesongfromalbum", (removesongfromalbum), methods=["GET"])
app.add_url_rule("/addsongtoalbum/<int:album_id>/<int:song_id>", "addsongtoalbum", (addsongtoalbum), methods=["GET"])
app.add_url_rule("/albumsbyuser/<int:user_id>", "albumsbyuser", (albumsbyuser), methods=["GET"])


# Artist endpoints
from resources.artist import ArtistResource
api.add_resource(ArtistResource, '/artists/<int:id>')


# Playlist endpoints
from resources.playlist import PlaylistResource, addsongtopl, removesongfrompl, showpl
api.add_resource(PlaylistResource, '/playlists/<int:id>', '/playlists/<int:user_id>/<int:pl_id>')
app.add_url_rule('/showpl/<int:pl_id>', "showPlaylist",(showpl), methods=["GET"])
app.add_url_rule('/addsongtopl/<int:pl_id>/<int:song_id>', "addSongtoPlaylist", (addsongtopl), methods=["GET"])
app.add_url_rule('/removesongfrompl/<int:pl_id>/<int:song_id>', "removesongfromplaylist", (removesongfrompl), methods=["GET"])


#Rating endpoints
from resources.rating import SubmitRatingResource
api.add_resource(SubmitRatingResource, '/rating/<int:song_id>/<int:user_id>')

