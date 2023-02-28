from engine import dp, scheduler
from .core import alarm1#,alarm2


def setup():
    scheduler.add_job(alarm1, 'cron' ,minute='*/2', args =(dp,))
