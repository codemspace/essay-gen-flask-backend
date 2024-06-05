from flask_apscheduler import APScheduler
from src.models.subscription_model import Subscription
from src import app, db

scheduler = APScheduler()

def reset_quota_usage():
    with app.app_context():
        db.session.query(Subscription).update({Subscription.quota_usage: 0 })
        db.session.commit()

scheduler.add_job(id='reset_quota_usage', func=reset_quota_usage, trigger='cron', hour=0, timezone='EST')
# scheduler.add_job(id='reset_quota_usage', func=reset_quota_usage, trigger='interval', seconds=5)