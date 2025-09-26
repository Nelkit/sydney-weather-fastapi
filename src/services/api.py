import openmeteo_requests

import requests_cache
from retry_requests import retry
from src.services.constants import BASE_API_URL, DEFAULT_TIMEZONE
from src.services.exceptions import OpenMeteoAPIError


class OpenMeteoApi():
	def __init__(self, latitude, longitude, start_date, end_date, daily_variables, hourly_variables,
				 timezone=DEFAULT_TIMEZONE):
		self.latitude = latitude
		self.longitude = longitude
		self.start_date = start_date
		self.end_date = end_date
		self.timezone = timezone
		self.cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
		self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
		self.client = openmeteo_requests.Client(session=self.retry_session)
		self.url = f"{BASE_API_URL}/archive"
		self.params = {
			"latitude": self.latitude,
			"longitude": self.longitude,
			"start_date": self.start_date,
			"end_date": self.end_date,
			"daily": daily_variables,
			"hourly": hourly_variables,
			"timezone": self.timezone
		}

	def fetch_data(self):
		try:
			responses = self.client.weather_api(self.url, params=self.params)
		except Exception as e:
			# Podrías parsear el dict del error si es un JSON
			raise OpenMeteoAPIError(
				message="Failed to fetch data from Open-Meteo",
				reason=str(e)
			)
		return responses