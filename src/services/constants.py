DEFAULT_LAT = -33.8688
DEFAULT_LON = 151.2093
DEFAULT_TIMEZONE = "Australia/Sydney"
BASE_API_URL = "https://archive-api.open-meteo.com/v1"

class RainOrNot:
	MODEL_PATH = "models/rain_or_not/best_model_v7.rc2.joblib"

	HOURLY_VARS = [
		"temperature_2m",
		"pressure_msl",
		"wind_speed_10m",
		"wind_direction_10m",
		"wind_gusts_10m",
		"cloud_cover",
		"cloud_cover_mid",
		"cloud_cover_low",
		"cloud_cover_high",
		"surface_pressure",
		"vapour_pressure_deficit",
		"relative_humidity_2m",
		"dew_point_2m",
		"precipitation",
		"rain",
		"boundary_layer_height",
		"wet_bulb_temperature_2m",
		"total_column_integrated_water_vapour"
	]

	DAILY_VARS = [
		"weather_code",
		"temperature_2m_mean",
		"temperature_2m_max",
		"temperature_2m_min",
		"precipitation_sum",
		"rain_sum",
		"snowfall_sum",
		"precipitation_hours",
		"wind_speed_10m_max",
		"wind_speed_10m_mean",
		"wind_gusts_10m_max",
		"wind_gusts_10m_mean",
		"wind_direction_10m_dominant",
		"relative_humidity_2m_mean",
		"relative_humidity_2m_min",
		"relative_humidity_2m_max",
		"pressure_msl_mean",
		"pressure_msl_max",
		"pressure_msl_min",
		"dew_point_2m_min",
		"dew_point_2m_max",
		"dew_point_2m_mean",
		"cloud_cover_min",
		"cloud_cover_max",
		"cloud_cover_mean",
		"surface_pressure_mean",
		"wet_bulb_temperature_2m_min",
		"wet_bulb_temperature_2m_max",
		"wet_bulb_temperature_2m_mean",
	]

	FEATURE_LIST = [
		'date',
		'cloud_cover_mean',
		'cloud_cover_min',
		'dew_point_2m_max',
		'dew_point_2m_mean',
		'dew_point_2m_min',
		'h_boundary_layer_height_max',
		'h_dew_point_2m_max',
		'h_dew_point_2m_mean',
		'h_dew_point_2m_min',
		'h_precipitation_mean',
		'h_rain_mean',
		'h_rain_sum',
		'h_temperature_2m_max',
		'h_temperature_2m_mean',
		'h_temperature_2m_min',
		'h_temperature_2m_std',
		'h_total_column_integrated_water_vapour_max',
		'h_total_column_integrated_water_vapour_mean',
		'h_vapour_pressure_deficit_max',
		'h_vapour_pressure_deficit_mean',
		'h_wet_bulb_temperature_2m_max',
		'h_wet_bulb_temperature_2m_mean',
		'h_wet_bulb_temperature_2m_min',
		'h_wind_gusts_10m_max',
		'h_wind_speed_10m_max',
		'precipitation_hours',
		'precipitation_sum',
		'pressure_msl_max',
		'relative_humidity_2m_max',
		'relative_humidity_2m_mean',
		'relative_humidity_2m_min',
		'rain_sum',
		'temperature_2m_max',
		'temperature_2m_mean',
		'temperature_2m_min',
		'wet_bulb_temperature_2m_max',
		'wet_bulb_temperature_2m_mean',
		'wet_bulb_temperature_2m_min',
		'weather_code',
		'wind_direction_10m_dominant',

		'wind_speed_10m_max',
		'wind_speed_10m_mean'
	]

class Precipitation:
	MODEL_PATH= "models/precipitation_fall/best_model_v3.rc2.joblib"

	HOURLY_VARS = [
		"apparent_temperature",
		"cloud_cover",
		"cloud_cover_high",
		"cloud_cover_low",
		"cloud_cover_mid",
		"dew_point_2m",
		"precipitation",
		"pressure_msl",
		"rain",
		"relative_humidity_2m",
		"snow_depth",
		"snowfall",
		"soil_moisture_0_to_7cm",
		"soil_moisture_7_to_28cm",
		"surface_pressure",
		"temperature_2m",
		"weather_code",
		"wind_gusts_10m",
		"wind_speed_10m",
		"wind_speed_100m"
	]

	DAILY_VARS = [
		"et0_fao_evapotranspiration",
		"precipitation_hours",
		"precipitation_sum",
		"rain_sum",
		"snowfall_sum",
		"soil_moisture_0_to_100cm_mean",
		"soil_moisture_0_to_7cm_mean",
		"soil_temperature_0_to_100cm_mean",
		"vapour_pressure_deficit_max",
		"wet_bulb_temperature_2m_mean",
		"wind_gusts_10m_max",
		"wind_speed_10m_max"
	]

	FEATURE_LIST = [
		'date',
		'd_precipitation_sum',
		'd_precipitation_hours',
		'd_wind_gusts_10m_max',
		'd_vapour_pressure_deficit_max',
		'd_et0_fao_evapotranspiration',
		'd_soil_moisture_0_to_100cm_mean',
		'd_soil_moisture_0_to_7cm_mean',
		'h_precipitation_sum',
		'h_relative_humidity_2m_mean',
		'h_temperature_2m_std',
		'h_cloud_cover_mean',
		'h_cloud_cover_max',
		'h_cloud_cover_high_mean',
		'h_cloud_cover_mid_mean',
		'h_cloud_cover_low_mean',
		'h_pressure_msl_mean',
		'h_wind_speed_10m_mean',
		'h_weather_code',
	]

