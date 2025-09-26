from fastapi import FastAPI, Query, HTTPException
from starlette.responses import HTMLResponse
import pandas as pd
import numpy as np
import cloudpickle
from joblib import load
from dskit_uts25609227.models.evaluation import calculate_classification_metrics
from src.services.api import OpenMeteoApi
from src.services.constants import (
	DEFAULT_LAT,
	DEFAULT_LON,
	RainOrNot,
	Precipitation
)
from src.services.exceptions import OpenMeteoAPIError
from src.services.preprocessor import DataPreprocessor, aggregate_rain_or_not_dataframe, aggregate_precipitation_fall_dataframe
from datetime import datetime
app = FastAPI()
rain_or_not_model = load(RainOrNot.MODEL_PATH)
precipitation_model = load(Precipitation.MODEL_PATH)

@app.get("/", response_class=HTMLResponse)
async def root():
	html_content = """
    <html>
        <head>
            <title>AMLA-AT2 Meteo API</title>
        </head>
        <body>
            <h1>AMLA-AT2 Meteo API</h1>
            <p>This API provides weather predictions for Sydney using machine learning models trained on historical Open-Meteo data.</p>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><code>/</code> - Project description and endpoints</li>
                <li><code>/health/</code> - API health check</li>
                <li><code>/predict/rain/?date=YYYY-MM-DD</code> - Predict if it will rain in exactly 7 days</li>
                <li><code>/predict/precipitation/fall?date=YYYY-MM-DD</code> - Predict cumulative precipitation over the next 3 days</li>
            </ul>
            <h2>Repository:</h2>
            <p><a href="https://github.com/Nelkit/AMLA-AT2-meteo-api-25609227">GitHub Repository</a></p>
        </body>
    </html>
    """
	return html_content

@app.get("/health/")
async def health_check():
	return {"status": "ok"}

@app.get("/predict/rain/")
async def predict_rain(date: str):
	try:
		_ = datetime.strptime(date, "%Y-%m-%d").date()
	except ValueError:
		raise HTTPException(
			status_code=400,
			detail={
				"error": "Invalid date format",
				"reason": "Use YYYY-MM-DD"
			}
		)

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

	features_df = aggregate_rain_or_not_dataframe(df_hourly, df_daily)

	# Select features
	X = features_df[RainOrNot.FEATURE_LIST].copy()

	X_temp = X.copy()

	for name, step in rain_or_not_model.steps:
		print(f"Step: {name}")
		# Algunos steps no tienen transform (p.ej. el clasificador final)
		if hasattr(step, "transform"):
			X_temp = step.transform(X_temp)
			print("Shape after step:", X_temp.shape)
			print(X_temp.head(1).to_dict(orient="records")[0])
			return
		else:
			print(f"{name} is final estimator, skipping transform.")

	# Predict
	y_pred = rain_or_not_model.predict(X)
	will_rain = bool(y_pred[0])

	# Build response
	prediction_date = (X["date"].iloc[0] + pd.Timedelta(days=7)).strftime("%Y-%m-%d")

	return {
		"input_date": date,
		"prediction": {
			"date": prediction_date,
			"will_rain": will_rain,
		}
	}

@app.get("/predict/precipitation/fall")
async def predict_precipitation_fall(date: str):
	try:
		_ = datetime.strptime(date, "%Y-%m-%d").date()
	except ValueError:
		raise HTTPException(
			status_code=400,
			detail={
				"error": "Invalid date format",
				"reason": "Use YYYY-MM-DD"
			}
		)
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
	features_df = aggregate_precipitation_fall_dataframe(df_hourly, df_daily)

	# Select features
	X = features_df[Precipitation.FEATURE_LIST].copy()

	# Predict
	y_pred = precipitation_model.predict(X)
	precipitation_fall = y_pred[0]

	# Build response
	end_date = (X["date"].iloc[0] + pd.Timedelta(days=3)).strftime("%Y-%m-%d")
	print(precipitation_fall[0])

	return {
		"input_date": date,
		"prediction": {
			"start_date": date,
			"end_date_date": end_date,
			"precipitation_fall": precipitation_fall[0],
		}
	}

