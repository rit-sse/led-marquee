import urllib.request
import json

def get():
	weather_string = "Weather Unavailable"

	weather_url = "http://api.openweathermap.org/data/2.1/weather/city/5134086"
	request = urllib.request.urlopen(weather_url)
	weather_info = json.loads(request.read().decode("utf-8"))
	request.close

	if weather_info is not None:
		temp = str(k_to_f(weather_info['main']['temp']))
		state = str(weather_info['weather'][0]['main'])
		desc = str(weather_info['weather'][0]['description'])
		weather_string = temp + " degrees, " + state + " (" + desc + ")"
	
	return weather_string


def k_to_f(kelvin):
	return int((kelvin - 273.15)* 1.8000 + 32.0)