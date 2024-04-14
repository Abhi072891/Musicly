# create a task for reminder through Google Chat
from gspace_webhook import reminder_webhook, song_webhook
from mail_server import send_email
from model import db, User, Song, Album
from datetime import datetime, timedelta
from sqlalchemy import and_

def daily_reminders():
    # users = User.query.all()
    one_day_ago=datetime.now()-timedelta(days=1)
    users = User.query.filter(User.login_at>=one_day_ago).all()
    for user in users:        
        reminder_webhook(user.username)
        print(f"Reminder sent to {user.username}")

def new_song_release():
    one_day_ago=datetime.now()-timedelta(days=1)
    songs = Song.query.filter(Song.created_at<=one_day_ago).all()
    for song in songs:
        song_webhook(song.song_name)
        print(f'notification for song {song.song_name} sent')

def monthly_activity_report(user_id):
    creator=User.query.get(int(user_id))
    seven_days_ago=datetime.now()-timedelta(days=7)
    songs = Song.query.filter(and_(Song.user_id == int(user_id), Song.created_on >= seven_days_ago)).all()
    albums = Album.query.filter(and_(Album.user_id == int(user_id), Album.created_on >= seven_days_ago)).all()

    content_body = "<h1>Weekly Report</h1>"
    content_body += f"<h2>Creator: {creator.username}</h2>"

    if songs:
        content_body += "<h3>Songs created:</h3>"
        for song in songs:
            content_body += f"<p>{song.song_name} - Views: {song.pcount}, Rating: {song.rating}</p>"

    if albums:
        content_body += "<h3>Albums created:</h3>"
        for album in albums:
            content_body += f"<p>{album.album_name} - Views: {album.rcount}</p>"
    send_email(creator.email,"Weekly Report",content_body)
   
