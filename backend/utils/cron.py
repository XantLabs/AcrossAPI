"""Schedules deletion of old photos."""

from celery import Celery
from celery.schedules import crontab

from ..models import Photo, db

sched = Celery()


@sched.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Execute every morning at 7:30 a.m."""
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        test.s(),
    )


@sched.task
def deleteOld():
    """Delete all photos older than 24 hours."""
