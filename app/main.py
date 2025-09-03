from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {
		"url": "/",
		"method": "GET",
		"status_code": 200,
		"title": "Meteo API root",
		"message": "Welcome to the Meteo API",
		"version": "1.0.0"
	}

