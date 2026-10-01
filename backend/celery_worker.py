"""Celery worker / beat entrypoint.

    celery -A celery_worker.celery worker --loglevel=info --pool=solo
    celery -A celery_worker.celery beat   --loglevel=info
"""

from app import create_app
from celery_app import celery , init_celery

flask_app = create_app()
init_celery(flask_app)

import tasks