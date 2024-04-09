from app import celery_app
from celery.schedules import crontab
from task import tasks



@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Reminding users to login
    sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.daily_reminders.s())

    # # Update access logs
    # sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.update_access_logs.s())

    # # Monthly activity report
    # sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.monthly_activity_report.s())