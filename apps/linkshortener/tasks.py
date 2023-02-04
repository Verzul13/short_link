import logging


from config.celery import app

logger = logging.getLogger("django")


@app.task
def test_task() -> None:
    logger.info('test loggging')
    print('======== yes')
