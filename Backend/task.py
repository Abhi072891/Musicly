# create a task for reminder through Google Chat
from gspace_webhook import reminder_webhook
from model import db, User

def daily_reminders():
    users = User.query.all()
    for user in users:
        
        reminder_webhook(user.username)
        print(f"Reminder sent to {user.username}")


def monthly_activity_report():
    pass

   
