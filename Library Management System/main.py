from flask import Flask
from flask_security import Security
from application.models import db
from config import DevelopmentConfig
from application.resources import api
from application.sec import datastore
from application.worker import celery_init_app
from application.tasks import daily_reminder, monthly_report, auto_revoke
import flask_excel as excel
from celery.schedules import crontab
from application.instances import cache


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    cache.init_app(app)
    app.security = Security(app, datastore)
    with app.app_context():
        import application.views
    return app, datastore

app, datastore = create_app()
celery_app = celery_init_app(app)


@celery_app.on_after_configure.connect
def celery_jobs(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=7, minute=0), auto_revoke.s())
    sender.add_periodic_task(crontab(hour=17, minute=0), daily_reminder.s())
    sender.add_periodic_task(crontab(hour=10, minute=0, day_of_month=1), monthly_report.s())
    # sender.add_periodic_task(20, daily_reminder.s())
    #sender.add_periodic_task(60, monthly_report.s())


if __name__ == "__main__":
    app.run(debug=True,port=5100)