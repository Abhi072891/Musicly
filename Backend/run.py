from app import app
from model import db
from cache import cache
from celery import Celery, Task
from celery.schedules import crontab
from task import daily_reminders, new_song_release, monthly_activity_report

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.broker_url = "redis://localhost:6379/1"
    celery_app.conf.result_backend = "redis://localhost:6379/2"
    # celery_app.conf.timezone = "Asia/Kolkata"  
    celery_app.conf.timezone = "UTC"  
    celery_app.conf.broker_connection_retry_on_startup=True  
    
    return celery_app

celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*', hour='*'), daily_reminders.s()) 
    sender.add_periodic_task(crontab(minute='*', hour='*'), new_song_release.s())
    sender.add_periodic_task(crontab(minute='*', hour='*'), monthly_activity_report.s())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        cache.init_app(app)
        app.run(debug=True)
        