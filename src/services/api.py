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
		self.url = f"{BASE_API_URL}/archive"
		# Open-Meteo expects comma-separated strings for variable lists
		daily_vars_param = ",".join(daily_variables) if isinstance(daily_variables, (list, tuple)) else daily_variables
		hourly_vars_param = ",".join(hourly_variables) if isinstance(hourly_variables, (list, tuple)) else hourly_variables
		self.params = {
			"latitude": self.latitude,
			"longitude": self.longitude,
			"start_date": self.start_date,
			"end_date": self.end_date,
			"daily": daily_vars_param,
			"hourly": hourly_vars_param,
			"timezone": self.timezone
		}

	def fetch_data(self):
		try:
			response = self.retry_session.get(self.url, params=self.params, timeout=30)
			if response.status_code != 200:
				# Try to extract error message from API JSON
				try:
					err_body = response.json()
					reason = err_body.get("reason") or err_body.get("error") or response.text
				except Exception:
					reason = response.text
				raise OpenMeteoAPIError(
					message="Failed to fetch data from Open-Meteo",
					reason=f"HTTP {response.status_code}: {reason}"
				)
			return response.json()
		except OpenMeteoAPIError:
			raise
		except Exception as e:
			raise OpenMeteoAPIError(
				message="Failed to fetch data from Open-Meteo",
				reason=str(e)
			)