from json import dumps
from httplib2 import Http


def reminder_webhook(username):
    url = "https://chat.googleapis.com/v1/spaces/AAAA9i3xW2M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=7Is6fRMLnuvNgYTxAJdPcWh7DUDRhC6XMotLaivVy3o"

    app_message = {
        "text": f"Hi {username}, don't forget to visit the Music app to check out the latest songs and albums!",
    }
    
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)

def song_webhook(songname):
    url = "https://chat.googleapis.com/v1/spaces/AAAA9i3xW2M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=7Is6fRMLnuvNgYTxAJdPcWh7DUDRhC6XMotLaivVy3o"
    
    app_message = {
        "text" : f"A new song : {songname} has been released"
    }
    
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)

