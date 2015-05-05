#!/usr/bin/python

import pyowm

owm = pyowm.OWM('fecdc239c28bb186a0cef382e48e0901')

# Will it be sunny tomorrow at this time in Milan (Italy) ?
forecast = owm.daily_forecast("Milan,it")
tomorrow = pyowm.timeutils.tomorrow()
forecast.will_be_sunny_at(tomorrow)  # Always True in Italy, right? ;-)

# Search for current weather in London (UK)
#observation = owm.weather_at_place('London,uk')
observation = owm.weather_at_place('bergen,norway')
w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20, 
                              # status=Clouds>

# Weather details
w.get_wind()                  # {'speed': 4.6, 'deg': 330}
w.get_humidity()              # 87
t = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
print t

# Search current weather observations in the surroundings of 
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
observation_list = owm.weather_around_coords(-22.57, -43.12)

# Query for daily weather forecast for the next 14 days over London
fc = owm.daily_forecast('London,uk')
f = fc.get_forecast()
for weather in f:
    print (weather.get_reference_time('iso'),weather.get_status())

# Query for Hourly weather forecast for the next 14 days over London
fc = owm.three_hours_forecast('London,uk')
f = fc.get_forecast()
# print f.to_JSON()
for weather in f:
    print (weather.get_reference_time('iso'),weather.get_status())
    # print (weather.get_reference_time('iso'),weather.get_temperature(unit='celsius'))
