from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()

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
	return {
		"input_date": date,
		"prediction": {
			"date": "2023-01-08",
			"will_rain": True,
		}
	}

@app.get("/predict/precipitation/fall")
async def predict_precipitation_fall(date: str):
	return {
		"input_date": date,
		"prediction": {
			"start_date": "2023-01-02",
			"end_date_date": "2023-01-04",
			"precipitation_fall": "28.2",
		}
	}

