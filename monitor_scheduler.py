from apscheduler.schedulers.background import BackgroundScheduler

def init_scheduled_monitoring():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        SalesforceAuthMonitor().check_password_expiry,
        'interval',
        hours=12,  # Check twice daily
        misfire_grace_time=60
    )
    scheduler.start()