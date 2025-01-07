from celery_config import celery

@celery.task(bind=True)
def add(self, x, y):
    return x + y