FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./models /code/models

COPY ./src /code/src

COPY ./static /code/static

COPY ./templates /code/templates

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80

# End of Dockerfile

# To build the Docker image, use the command:
# docker build -t meteo-api-app .
# To run the Docker container, use the command:
# docker run -d -p 80:80 meteo-api-app