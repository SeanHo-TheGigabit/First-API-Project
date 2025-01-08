from app import celery_app as celery


@celery.task(bind=True)
def add(self, x, y):
    """Celery task to add two numbers

    ref: [Bound task meaning](https://stackoverflow.com/a/54899481)
    """
    return x + y

from celery import shared_task
import time


@shared_task(ignore_result=False)
def hello_world():
    for i in range(1, 6):
        print(i)
        time.sleep(1)

    print("Hello Celery")