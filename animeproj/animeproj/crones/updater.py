from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from anime.tasks import daily


def start():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        daily.my_post_migrate_handler,
        trigger=CronTrigger(hour=0, minute=0),
        id='refresh_views'
    )

    scheduler.start()
