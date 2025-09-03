# AMLA-AT2-meteo-api-25609227

**Description:**  
FastAPI application that provides weather data through REST API endpoints. Fetches information from external sources and serves it to clients for easy access and integration.  

---

## Table of Contents

- [Installation](#installation)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [Development](#development)  
- [License](#license)  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Nelkit/AMLA-AT2-meteo-api-25609227.git

cd AMLA-AT2-meteo-api-25609227
```
2. Set Python version (if not already set):

```bash
 pyenv install 3.11.4
 pyenv local  3.11.4
```

3. activate the poetry environment

```bash
poetry env activate
```

4. Install dependencies with Poetry:

```bash
poetry install
```

## Usage

Run the FastAPI server:
```bash
poetry run uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000 to see the API documentation.

## API Endpoints
| Method | Endpoint          | Description                  |
| ------ | ----------------- | ---------------------------- |
| GET    | `/`               | Returns a welcome message    |
| GET    | `/weather`        | Retrieves weather data       |
| GET    | `/weather/{city}` | Retrieves weather for a city |

Detailed documentation is available automatically at http://127.0.0.1:8000/docs
 via Swagger UI.

## Development

- Use --reload for automatic server restart during development.

- Place all your FastAPI routes inside the app/ folder.

- Add dependencies via Poetry:

```bash 
poetry add <package-name>
```


## License

This project is licensed under the MIT License.


