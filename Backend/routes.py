from flask import request, render_template, url_for, redirect
from sqlalchemy import func
from app import app, db
from model import *
from form import *
import os

@app.route("/")
def index():
    admin=Login.query.get(1)
    if not admin:
        admin=Login(name="admin",username="admin",password="admin")
        db.session.add(admin)
        db.session.commit()
    return render_template("index.html")


@app.route('/home/<int:id>',methods=['GET','POST'])
def home(id):
    if request.method=="POST":
        search_type=request.form.get('search-type')
        query=request.form.get('query')
        
        if search_type == "song":
            songs = Song.query.filter(Song.song_name.ilike(f'%{query}%')).all()
            if not songs:
                return f'No Macth Found <a href="/home/{id}">Go Back</a>'
            return render_template('search.html', songs=songs)

        elif search_type == "album":
            albums = Album.query.filter(Album.album_name.ilike(f'%{query}%')).all()
            if not albums:
                return f'No Macth Found <a href="/home/{id}">Go Back</a>'
            return render_template('search.html', albums=albums)

        elif search_type == "artist":
            artists = Artist.query.filter(Artist.artist_name.ilike(f'%{query}%')).all()
            if not artists:
                return f'No Macth Found <a href="/home/{id}">Go Back</a>'
            return render_template('search.html', artists=artists)
        

    top_song=Song.query.order_by(Song.pcount.desc()).limit(10).all()
    top_artist=Artist.query.order_by(Artist.scount.desc()).limit(10).all()
    top_album=Album.query.order_by(Album.rcount.desc()).limit(10).all()
    all_genres = ["Pop", "Rock", "Hip-Hop", "Jazz", "Country", "Electronic", "R&B", "Reggae", "Classical", "Blues", "Metal", "Alternative", "Indie", "Folk", "Punk", "Other"]
    user=Login.query.get(id)
    return render_template('base.html',user_id=id,top_song=top_song,top_artist=top_artist,top_album=top_album,role=user.role,all_genres=all_genres)

@app.route('/genre/<genre_name>/<int:user_id>')
def genre_songs(genre_name,user_id):
    songs = Song.query.filter_by(song_genre=genre_name).all()
    if not songs:
        return f'No song in this Genre <a href="/home/{user_id}">Go back<a/>'
    return render_template('genre_songs.html', genre=genre_name, songs=songs,user_id=user_id)

@app.route("/upload/<int:user_id>", methods=["GET","POST"])
def upload(user_id):
    if request.method=='POST':
        s=Song.query.filter_by(song_name=request.form.get('songname')).all()
        if s:
            return f'Songname already Exists <a href="/upload/{user_id}">Go back </a>'

        if 'songfile' in request.files:
            songfile = request.files['songfile']
            songfile.save('static/music/'+songfile.filename)
            songname=request.form.get('songname')
            song = Song(song_name=songname,song_path='static/music/'+songfile.filename,rating=0,pcount=0,user_id=int(user_id))
            db.session.add(song)

            if request.form.get('artistname'):
                artist_names = [name.strip() for name in request.form.get('artistname').split(',')]
                for artist_name in artist_names:
                    artist = Artist.query.filter(func.lower(Artist.artist_name) == func.lower(artist_name)).first()
                    if not artist:
                        artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                        db.session.add(artist)
                    song.artists.append(artist)
                    artist.songs.append(song)
            
            if request.form.get('genre')!='none':
                song.song_genre=request.form.get('genre')

            
            if request.form.get('lyrics'):
                song.song_lyrics=request.form.get('lyrics')

            if request.form.get('album')!='none':
                if request.form.get('album')=='new':
                    a_name=request.form.get('new_album_name')
                    n_album= Album(album_name=a_name,rcount=0,user_id=user_id)
                    n_album.songs.append(song)
                    song.albums.append(n_album)
                else:
                    album=Album.query.filter_by(album_name=request.form.get('album')).one()
                    song.albums.append(album)

            db.session.commit()
            songs=Song.query.filter_by(user_id=user_id).all()
            albums=Album.query.filter_by(user_id=user_id).all()
            return render_template('creator.html',user_id=user_id,songs=songs,albums=albums,totalsong=len(songs),totalalbum=len(albums))


    else:
        albums=Album.query.all()
        return render_template('upload.html',albums=albums,user_id=user_id)
    
@app.route("/songs/<int:id>")
def allsongs(id):
    songs=Song.query.all()
    
    return render_template("songs.html",songs=songs,user_id=id)

@app.route('/songinfo/<int:songid>/<int:userid>')
def songinfo(songid,userid):
    song=Song.query.get(songid)
    song.pcount+=1
    db.session.commit()
    pl=Playlist.query.filter_by(user_id=userid).all()
    return render_template('songinfo.html',song=song,user_id=userid,rated=False,playlists=pl)


@app.route('/submit_rating/<int:song_id>/<int:user_id>', methods=['POST'])
def submit_rating(song_id,user_id):
    if request.method == 'POST':
        rate = request.form.get('rating')
        rentry = Rate.query.filter_by(userid=user_id,songid=song_id).first()
        if rentry:
            rentry.ratinggiven=rate
            db.session.commit()
        else:
            nentry=Rate(userid=user_id,songid=song_id,ratinggiven=rate)
            db.session.add(nentry)
            db.session.commit()

        song=Song.query.get(song_id)
        allrating=Rate.query.filter_by(songid=song_id).all()
        count=len(allrating)
        sum=0
        for i in allrating:
            sum+=int(i.ratinggiven)
        avgrating=sum/count
        song.rating=round(avgrating)
        db.session.commit()
        return render_template('songinfo.html',rated=True,song=song,user_id=user_id,ratevalue=rate)

@app.route('/albums/<int:user_id>')
def albums(user_id):
    albums=Album.query.all()
    return render_template('albums.html',albums=albums,user_id=user_id)

@app.route('/album/<int:album_id>/<int:user_id>')
def albuminfo(album_id,user_id):
    album=Album.query.get(album_id)
    album.rcount+=1
    db.session.commit()
    return render_template('albuminfo.html',album=album,user_id=user_id)


@app.route('/artists/<int:user_id>')
def artists(user_id):
    artists=Artist.query.all()
    return render_template('artists.html',artists=artists,user_id=user_id)

@app.route('/artist/<int:artist_id>/<int:user_id>')
def artistinfo(artist_id,user_id):
    artist=Artist.query.get(artist_id)
    artist.scount+=1
    db.session.commit()
    return render_template('artistinfo.html',artist=artist,user_id=user_id)

#playlist

@app.route('/playlist/<int:user_id>', methods=["GET","POST"])
def playlist(user_id):
    if request.method=='POST':
        pl_id = request.form.get('playlist_id')
        song_ids = request.form.getlist('song_id[]')
        new_playlist_name = request.form.get('new_playlist_name')

        if pl_id == 'new':
            new_playlist = Playlist(user_id=user_id,playlist_name=new_playlist_name)
            db.session.add(new_playlist)
            db.session.commit()
            pl_id = new_playlist.playlist_id

        for song_id in song_ids:
            playlist_song = PlaylistContent(playlist_id=int(pl_id), song_id=song_id)
            db.session.add(playlist_song)
        db.session.commit()

        plsongs=[]
        plcontent=PlaylistContent.query.filter_by(playlist_id=pl_id).all()
        for i in plcontent:
            plsongs.append(Song.query.get(i.song_id))
        return render_template('showpl.html',user_id=user_id,songs=plsongs,pl_id=pl_id)

    playlists=Playlist.query.filter_by(user_id=user_id).all()
    songs=Song.query.all()
    return render_template('plist.html',user_id=user_id,songs=songs,playlists=playlists)

@app.route('/allplaylist/<int:user_id>')
def allplaylist(user_id):
    playlists=Playlist.query.filter_by(user_id=user_id).all()
    return render_template('allplaylists.html',playlists=playlists,user_id=user_id)

@app.route('/showpl/<int:user_id>/<int:pl_id>')
def showpl(user_id,pl_id):
    plsongs=[]
    plcontent=PlaylistContent.query.filter_by(playlist_id=pl_id).all()
    pl_name=Playlist.query.get(pl_id).playlist_name
    for i in plcontent:
        plsongs.append(Song.query.get(i.song_id))
    return render_template('showpl.html',user_id=user_id,songs=plsongs,pl_name=pl_name,pl_id=pl_id)

@app.route('/removesongfrompl/<int:user_id>/<int:pl_id>/<int:song_id>')
def removesongfrompl(user_id,pl_id,song_id):
    data=PlaylistContent.query.filter_by(song_id=song_id, playlist_id=pl_id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect(f'/showpl/{user_id}/{pl_id}')

@app.route('/addtoplaylist/<int:user_id>/<int:song_id>', methods=["GET","POST"])
def addtoplaylist(user_id,song_id, methods=["GET","POST"]):
    if request.method=="POST":
        pl_id=int(request.form.get('pl_id'))
        data=PlaylistContent.query.filter_by(song_id=song_id, playlist_id=pl_id).first()
        if not data:
            playlist_song = PlaylistContent(playlist_id=int(pl_id), song_id=song_id)
            db.session.add(playlist_song)
            db.session.commit()
        return redirect(f'/songinfo/{song_id}/{user_id}')

@app.route('/deletepl/<int:user_id>/<int:pl_id>',methods=['GET','POST'])
def deletepl(user_id,pl_id):
    playlist = Playlist.query.get(pl_id)
    if playlist:
        db.session.delete(playlist)
        data=PlaylistContent.query.filter_by(playlist_id=pl_id).all()
        if data:
            for i in data:
                db.session.delete(i)
        db.session.commit()
    playlists=Playlist.query.filter_by(user_id=user_id).all()
    return render_template('allplaylists.html',playlists=playlists,user_id=user_id)


#Login

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    text=""
    if request.method=="POST":
        user = Login.query.filter_by(username=form.username.data).first()
        if not user:
            text="Not a User or wrong Username : "
            return render_template('login.html', form=form, text=text)
        if form.password.data!=user.password:
            text="wrong Password try again"
            return render_template('login.html', form=form, text=text)
        return redirect(f'/home/{user.login_id}')
    return render_template('login.html', form=form, text=text)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    text = ""
    if request.method=="POST":
        temp = Login.query.filter_by(username=form.username.data).first()
        if temp:
            text = "Username already exists"
        else:
            user = Login(name=form.name.data,username=form.username.data, password=form.password.data, role=0)
            db.session.add(user)
            if form.age.data:
                user.age=form.age.data
            if form.gender.data!='Prefer not to say':
                user.gender=form.gender.data
            db.session.commit()
            # return render_template('login.html', form=form, text=text)
            return redirect('login')
    return render_template('register.html', form=form, text=text)

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    text=''
    if request.method=="POST":
        if request.form.get('uname')=='Abhishek1196':
            if request.form.get('password')=='100600':
                data=[]
                data.append(int(db.session.query(Login).count())-1)
                data.append(db.session.query(Login).filter(Login.role == 1).count())
                data.append(db.session.query(Song).count())
                data.append(db.session.query(Album).count())
                return render_template('admindashboard.html',data=data)
            else:
                text='Wrong Password Try Again'
                return render_template('adminlogin.html',text=text)
        else:
            text="Wrong UserName Try Again"
            return render_template('adminlogin.html',text=text)
    return render_template('adminlogin.html',text=text)



# Creator
@app.route('/creator/<int:user_id>')
def creator(user_id):
    creator=Login.query.get(user_id)
    if creator.role==2:
        return f'You have been Blacklisted by Admin from being a Creator <a href="/home/{user_id}">Go Back</a>'
    songs=Song.query.filter_by(user_id=user_id).all()
    albums=Album.query.filter_by(user_id=user_id).all()
    return render_template('creator.html',user_id=user_id,songs=songs,albums=albums,totalsong=len(songs),totalalbum=len(albums))

@app.route('/creatorregister/<int:user_id>',methods=["GET","POST"])
def creatorregister(user_id):
    user=Login.query.get(int(user_id))
    text=""
    if request.method=="POST":
        if request.form.get('password')==user.password:    
            user.role=1
            db.session.commit()
            return redirect(f'/home/{user.login_id}')
        else:
            text="Wrong Password Try Again"
            return render_template('creatorregister.html',user_id=user_id,uname=user.username,name=user.name,text=text)        
    return render_template('creatorregister.html',user_id=user_id,uname=user.username,name=user.name)


@app.route('/deletesong/<int:user_id>/<int:song_id>',methods=['GET','POST'])
def deletesong(user_id,song_id):
    song = Song.query.get(song_id)
    if song:
        data=Rate.query.filter_by(songid=song_id).all()
        if data:
            for i in data:
                db.session.delete(i)

        data2=PlaylistContent.query.filter_by(song_id=song_id).all()
        if data2:
            for i in data2:
                db.session.delete(i)

        os.remove(os.path.join(app.root_path, song.song_path))
        db.session.delete(song)
        db.session.commit()
    songs=Song.query.filter_by(user_id=user_id).all()
    albums=Album.query.filter_by(user_id=user_id).all()
    if int(user_id)==1:
        return redirect('/admindashboard') 
    return render_template('creator.html',user_id=user_id,songs=songs,albums=albums,totalsong=len(songs),totalalbum=len(albums))


@app.route('/editsong/<int:user_id>/<int:song_id>',methods=['GET','POST'])
def editsong(user_id,song_id):
    song=Song.query.get(int(song_id))
    if request.method=='POST':
        song.song_name=request.form.get('song_name')
        song.song_genre=request.form.get('genre')
        song.song_lyrics=request.form.get('song_lyrics')
        artist_names = [name.strip() for name in request.form.get('artistname').split(',')]
        for artist_name in artist_names:
            artist = Artist.query.filter(func.lower(Artist.artist_name) == func.lower(artist_name)).first()
            if not artist:
                artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                db.session.add(artist)
            song.artists.append(artist)
            artist.songs.append(song)

        if request.form.get('album')=='new':
            a_name=request.form.get('new_album_name')
            n_album= Album(album_name=a_name,rcount=0,user_id=user_id)
            n_album.songs.append(song)
            song.albums.append(n_album)
        elif request.form.get('album')=='none':
            song.albums=[]
        elif request.form.get('album')=='nochange':
            pass
        else:
            album=Album.query.filter_by(album_name=request.form.get('album')).one()
            song.albums.append(album)
        db.session.commit()
        return redirect(f'/creator/{user_id}')
            
    artists=song.artists
    artistnames=''
    artistnames = ','.join(artist.artist_name for artist in artists).rstrip(',')

    albums=song.albums
    albumnames=''
    albumnames = ','.join(album.album_name for album in albums).rstrip(',')
    allalbums=Album.query.all()

    return render_template('editsong.html',song=song,artist=artistnames,album=albumnames,albums=allalbums,user_id=user_id)

@app.route('/editalbum/<int:album_id>/<int:user_id>',methods=['GET','POST'])
def editalbum(user_id,album_id):
    album=Album.query.get(int(album_id))
    if request.method=="POST":
        song_ids = request.form.getlist('song_id[]')
        if song_ids:
            for song_id in song_ids:
                song=Song.query.get(song_id)
                album.songs.append(song)
        if request.form.get('artistname'):
            artist_names = [name.strip() for name in request.form.get('artistname').split(',')]
            for artist_name in artist_names:
                artist = Artist.query.filter(func.lower(Artist.artist_name) == func.lower(artist_name)).first()
                if not artist:
                    artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                    db.session.add(artist)
                album.artists.append(artist)
        db.session.commit()
        return redirect(f'/creator/{user_id}')

    temp=album_id
    # songs_not_in_album = Song.query.filter(Song.albums.any(album_id != temp)).all()
    songs_not_in_album = Song.query.filter(~Song.albums.any(album_id=temp)).all()
    songs_in_album=album.songs
    artists=album.artists
    artistnames = ','.join(artist.artist_name for artist in artists).rstrip(',')
    return render_template('editalbum.html',album=album,artist=artistnames,addsongs=songs_not_in_album,removesongs=songs_in_album,user_id=user_id)

@app.route('/removesongfromalbum/<int:album_id>/<int:song_id>/<int:user_id>')
def removesongfromalbum(album_id,song_id,user_id):
    song=Song.query.get(song_id)
    album=Album.query.get(album_id)
    song.albums.remove(album)
    db.session.commit()
    return redirect(f'/editalbum/{album_id}/{user_id}')

@app.route('/createalbum/<int:user_id>',methods=['GET','POST'])
def createalbum(user_id):
    songs=Song.query.all()
    if request.method=="POST":
        al=Album.query.filter_by(album_name=request.form.get('album_name')).one()
        if al:
            return f'Albumname already Exists <a href="/createalbum/{user_id}">Go back</a>'
        album=Album(album_name=request.form.get('album_name'),user_id=user_id)
        db.session.add(album)
        song_ids = request.form.getlist('song_id[]')
        if song_ids:
            for song_id in song_ids:
                song=Song.query.get(song_id)
                album.songs.append(song)
        if request.form.get('artistname'):
            artist_names = [name.strip() for name in request.form.get('artistname').split(',')]
            for artist_name in artist_names:
                artist = Artist.query.filter(func.lower(Artist.artist_name) == func.lower(artist_name)).first()
                if not artist:
                    artist = Artist(artist_name=artist_name, scount=0, user_id=user_id)
                    db.session.add(artist)
                album.artists.append(artist)
        db.session.commit()
        return redirect(f'/creator/{user_id}')
    return render_template('createalbum.html',songs=songs,user_id=user_id,rcount=0)


@app.route('/deletealbum/<int:user_id>/<int:album_id>',methods=['GET','POST'])
def deletealbum(user_id,album_id):
    album = Album.query.get(album_id)
    if album:
        db.session.delete(album)
        db.session.commit()
    songs=Song.query.filter_by(user_id=user_id).all()
    albums=Album.query.filter_by(user_id=user_id).all()
    if int(user_id)==1:
        return redirect('/admindshboard') 
    return render_template('creator.html',user_id=user_id,songs=songs,albums=albums,totalsong=len(songs),totalalbum=len(albums))



#Admin
@app.route('/admindashboard')
def admindashboard():
    data=[]
    data.append(int(db.session.query(Login).count())-1)
    data.append(db.session.query(Login).filter((Login.role==1)|(Login.role==2)).count())
    data.append(db.session.query(Song).count())
    data.append(db.session.query(Album).count())
    return render_template('admindashboard.html',data=data)

@app.route('/adminalbums')
def adminalbums():
    albums=Album.query.all()
    return render_template('adminalbums.html',albums=albums)

@app.route('/adminsongs')
def adminsongs():
    songs=Song.query.all()
    return render_template("adminsongs.html",songs=songs)

@app.route('/admincreators')
def admincreators():
    creators=db.session.query(Login).filter((Login.role==1) | (Login.role==2)).all()
    return render_template('admincreators.html',creators=creators)

@app.route('/creatorinfo/<int:id>')
def creatorinfo(id):
    creator=Login.query.get(id)
    songs=Song.query.filter_by(user_id=id).all()
    albums=Album.query.filter_by(user_id=id).all()
    return render_template('creatorinfo.html',creator=creator,songs=songs,albums=albums)

@app.route('/blacklist/<int:id>')
def blacklist(id):
    creator=Login.query.get(id)
    creator.role=2
    db.session.commit()
    return redirect(url_for('admincreators'))

@app.route('/whitelist/<int:id>')
def whitelist(id):
    creator=Login.query.get(id)
    creator.role=1
    db.session.commit()
    return redirect(url_for('admincreators'))
