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

