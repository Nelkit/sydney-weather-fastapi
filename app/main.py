import pandas as pd
from joblib import load
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from src.services.api import OpenMeteoApi
from src.services.constants import (
	DEFAULT_LAT,
	DEFAULT_LON,
	RainOrNot,
	Precipitation
)
from src.services.exceptions import OpenMeteoAPIError
from src.services.preprocessor import (
	DataPreprocessor,
	join_rain_data,
	join_precipitation_data
)
from src.utils.validation import validate_date, validate_date_range

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

rain_or_not_model = load(RainOrNot.MODEL_PATH)
precipitation_model = load(Precipitation.MODEL_PATH)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health/")
async def health_check():
	return {
		"status": "ok",
		"message": "The service is running.",
		"models": {
			"rain_or_not": {
				"version": RainOrNot.MODEL_VERSION,
			},
			"precipitation_fall": {
				"version": Precipitation.MODEL_VERSION,
			}
		}
	}

@app.get("/predict/rain/")
async def predict_rain(date: str):
	validate_date(date)
	validate_date_range(date, earliest_date="1940-01-01")

	# Fetch weather data from Open-Meteo API
	api = OpenMeteoApi(
		latitude=DEFAULT_LAT,
		longitude=DEFAULT_LON,
		start_date=date,
		end_date=date,
		daily_variables=RainOrNot.DAILY_VARS,
		hourly_variables=RainOrNot.HOURLY_VARS
	)
	try:
		raw_data = api.fetch_data()
	except OpenMeteoAPIError as e:
		raise HTTPException(
			status_code=400,
			detail={
				"error": "Open-Meteo API request failed",
				"reason": e.reason
			}
		)
	except Exception:
		raise HTTPException(
			status_code=500,
			detail="Internal server error"
		)

	# Preprocess data
	preprocessor = DataPreprocessor(
		raw_data,
		RainOrNot.HOURLY_VARS,
		RainOrNot.DAILY_VARS
	)
	df_hourly, df_daily = preprocessor.preprocess_weather_data()

	features_df = join_rain_data(df_daily, df_hourly)

	# Select features
	x = features_df[RainOrNot.FEATURE_LIST].copy()

	# Predict
	y_pred = rain_or_not_model.predict(x)
	will_rain = bool(y_pred[0])

	# Build response
	prediction_date = (x["date"].iloc[0] + pd.Timedelta(days=7)).strftime("%Y-%m-%d")

	return {
		"input_date": date,
		"prediction": {
			"date": prediction_date,
			"will_rain": will_rain,
		}
	}

@app.get("/predict/precipitation/fall")
async def predict_precipitation_fall(date: str):
	validate_date(date)
	validate_date_range(date, earliest_date="1940-01-01")

	# Fetch weather data from Open-Meteo API
	api = OpenMeteoApi(
		latitude=DEFAULT_LAT,
		longitude=DEFAULT_LON,
		start_date=date,
		end_date=date,
		daily_variables=Precipitation.DAILY_VARS,
		hourly_variables=Precipitation.HOURLY_VARS
	)
	try:
		raw_data = api.fetch_data()
	except OpenMeteoAPIError as e:
		raise HTTPException(
			status_code=400,
			detail={
				"error": "Open-Meteo API request failed",
				"reason": e.reason
			}
		)
	except Exception:
		raise HTTPException(
			status_code=500,
			detail="Internal server error"
		)
	# Preprocess data
	preprocessor = DataPreprocessor(
		raw_data,
		Precipitation.HOURLY_VARS,
		Precipitation.DAILY_VARS
	)
	df_hourly, df_daily = preprocessor.preprocess_weather_data()
	features_df = join_precipitation_data(df_daily, df_hourly)

	# Select features
	x = features_df[Precipitation.FEATURE_LIST].copy()

	# Predict
	y_pred = precipitation_model.predict(x)
	precipitation_fall = y_pred[0]

	# Build response
	end_date = (x["date"].iloc[0] + pd.Timedelta(days=3)).strftime("%Y-%m-%d")

	return {
		"input_date": date,
		"prediction": {
			"start_date": date,
			"end_date": end_date,
			"precipitation_fall": f"{precipitation_fall:.4f} mm",
		}
	}

