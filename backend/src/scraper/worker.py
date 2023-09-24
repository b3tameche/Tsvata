import os
import logging

from celery.schedules import crontab
from celery import signature, chord
from sqlalchemy import text

from celery_app import celery_app
from constants import TASKS_FILE_NAMES, TASKS_DIR

logger = logging.getLogger(__name__)

def register_tasks():
    for filename in TASKS_FILE_NAMES:
        celery_app.autodiscover_tasks(['units'], related_name=filename[:-3], force=True)

@celery_app.task(name='job-saver')
def store_jobs(queries: list[list[dict[str, str]]]):
    from sessioncontext import create_session # should be imported after celery_app.autodiscover_tasks

    with create_session() as session:
        for subq in queries:
            for q in subq:
                title = q.get('title')
                url = q.get('url')
                company = q.get('company')
                skills = str(q.get('skills'))

                insert_job_sql = f'INSERT INTO jobs(title, company, url, skills) VALUES (\'{title}\', \'{company}\', \'{url}\', ARRAY{skills});'

                try:
                    session.execute(text(insert_job_sql))
                except Exception as e:
                    session.rollback()
                    logger.error(e)
        
        session.execute(text('DELETE FROM jobs WHERE timestamp <= NOW() - INTERVAL \'1 month\';'))
        session.commit()
                

@celery_app.task(name='job-scraper')
def execute_chain():
    chord(signature(os.path.join(TASKS_DIR, filename)) for filename in TASKS_FILE_NAMES)(store_jobs.s())

if __name__ == '__main__':
    register_tasks()

    # execute explicitly
    execute_chain.delay()

    celery_app.conf.beat_schedule.update({
            'scraper_schedule': {
                'task': 'job-scraper',
                'schedule': crontab(hour='17', minute='0') # 21-4 for UTC, every day at 21:00
            }
        })
    
    argv = [
        'worker', 
        '--loglevel=INFO',
        '-B'
    ]

    celery_app.worker_main(argv)


