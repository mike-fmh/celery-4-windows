import os
import logging
from celery import shared_task, current_task, Celery


USERNAME, PASSWORD, PORT, HOST = os.getenv('REDIS_USER'), os.getenv('REDIS_PASS'), os.getenv('REDIS_PORT'), os.getenv('REDIS_HOST')
print(USERNAME, PASSWORD, HOST, PORT)

logger = logging.getLogger(__name__)

app = Celery('app')
app.conf.update({
    'broker_url': f"amqp://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/",
    'broker_transport_options': {
        'data_folder_in': './broker/out',
        'data_folder_out': './broker/out',
        'data_folder_processed': './broker/processed'
    }})


# setup folder for message broking
for f in ['./broker/out', './broker/processed']:
    if not os.path.exists(f):
        os.makedirs(f)


@app.task()
def add(x, y):
    result = x + y
    logger.info(f'Add: {x} + {y} = {result}')
    return result


if __name__ == '__main__':
    task = add.s(x=2, y=3).delay()
    print(f'Started task: {task}')
