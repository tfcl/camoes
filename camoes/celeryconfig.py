
from celery import Celery
from celery.schedules import crontab

app = Celery()


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'library.tasks.add',
        'schedule': 10.0,
        'args': (16, 16)
    },
}
@app.task
def test(arg):
    print(arg)

broker_url = 'amqp://localhost'


timezone = 'Europe/Oslo'
enable_utc = True