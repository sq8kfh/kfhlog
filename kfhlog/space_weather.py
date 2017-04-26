import hamutils.space_weather
import datetime


class Space_weather:
    def __init__(self):
        self._predictions = hamutils.space_weather.get_space_weather_predictions()
        self._geomagnetic = hamutils.space_weather.get_geomagnetic_data()
        self._solar = hamutils.space_weather.get_solar_data()

    @property
    def predictions(self):
        date = datetime.datetime.now().date()
        if not self._predictions or self._predictions[0]['date'] < date:
            self._predictions = hamutils.space_weather.get_space_weather_predictions()
        return self._predictions

    @property
    def geomagnetic(self):
        date = datetime.datetime.now()
        if not self._geomagnetic or self._geomagnetic[-1]['date'] < date.date():
            self._geomagnetic = hamutils.space_weather.get_geomagnetic_data()
        else:
            time = None
            if not self._geomagnetic[-1]['Kp03']:
                time = datetime.time(3,0,0)
            elif not self._geomagnetic[-1]['Kp06']:
                time = datetime.time(6,0,0)
            elif not self._geomagnetic[-1]['Kp09']:
                time = datetime.time(9,0,0)
            elif not self._geomagnetic[-1]['Kp12']:
                time = datetime.time(12,0,0)
            elif not self._geomagnetic[-1]['Kp15']:
                time = datetime.time(15,0,0)
            elif not self._geomagnetic[-1]['Kp18']:
                time = datetime.time(18,0,0)
            elif not self._geomagnetic[-1]['Kp21']:
                time = datetime.time(21,0,0)
            if time:
                tmp = datetime.datetime.combine(self._geomagnetic[-1]['date'], time)
                if tmp < date:
                    self._geomagnetic = hamutils.space_weather.get_geomagnetic_data()
        return self._geomagnetic

    @property
    def solar(self):
        date = datetime.datetime.now().date()
        if not self._solar or self._solar[-1]['date'] < (date - datetime.timedelta(1)):
            self._solar = hamutils.space_weather.get_solar_data()
        return self._solar
