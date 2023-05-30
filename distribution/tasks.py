from notifications.celery import app

@app.task
def add(x, y):
    return (x + y)

app.conf.beat_schedule = {
    'run-every-5-seconds': {
        'task': 'tasks.add',
        'schedule': 5.0,
    },
}