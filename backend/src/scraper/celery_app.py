from celery import Celery

celery_app = Celery('bartholomeu', backend='redis://redis:6379/0', broker='redis://redis:6379/0')
