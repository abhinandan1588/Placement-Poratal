'''
Worker (Windows needs the solo pool):
    celery -A celery_worker.celery worker --loglevel=info --pool=solo

Scheduler:
    celery -A celery_worker.celery beat --loglevel=info
'''

from celery import Celery
from celery.schedules import crontab

from config import Config

celery = Celery(
    "Placement Portal", 
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND   
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {
    "daily-deadline-remainder":{
        "task":"tasks.send_monthly_reports",
        "schedule" : crontab(hour = 9, minute = 0)
    },
    "monthly-activity-report" : {
        "task" : "tasks.send_monthly_report",
        "schedule":crontab(day_of_month = 1 ,hour = 8 , minute = 0 )      
    }
}


def init_celery(app):
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self , *args , **kwargs)
    celery.Task = ContextTask
    return celery