from .basetask import BaseTask

from ..models import get_tm_session, Qso
from .. import space_weather
from pyramid_celery import celery_app

@celery_app.task(base=BaseTask, bind=True)
def update_space_weather(self):
    redis = self.get_redis()
    if 'space_weather' in redis:
        sp = redis['space_weather']
        sp.update()
    else:
        sp = space_weather.Space_weather()
    redis['space_weather'] = sp
