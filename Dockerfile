FROM python:3.12

WORKDIR /log-exporter

COPY ./requirements.txt /log-exporter/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /log-exporter/requirements.txt

COPY ./app /log-exporter/app

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]