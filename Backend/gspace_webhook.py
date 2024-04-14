from json import dumps
from httplib2 import Http

# Copy the webhook URL from the Chat space where the webhook is registered.
# The values for SPACE_ID, KEY, and TOKEN are set by Chat, and are included
# when you copy the webhook URL.

def reminder_webhook(username):
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAAA9i3xW2M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=7Is6fRMLnuvNgYTxAJdPcWh7DUDRhC6XMotLaivVy3o"
    
    # reminder message for the user to visit the Music app
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
    """Google Chat incoming webhook quickstart."""
    url = "https://chat.googleapis.com/v1/spaces/AAAA9i3xW2M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=7Is6fRMLnuvNgYTxAJdPcWh7DUDRhC6XMotLaivVy3o"
    
    # reminder message for the user to visit the Music app
    app_message = {
        # "text": f"Hi {username}, don't forget to visit the Music app to check out the latest songs and albums!",
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

