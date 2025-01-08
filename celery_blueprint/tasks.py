from app import celery_app as celery


@celery.task(bind=True)
def add(self, x, y):
    """Celery task to add two numbers

    ref: [Bound task meaning](https://stackoverflow.com/a/54899481)
    """
    return x + y
