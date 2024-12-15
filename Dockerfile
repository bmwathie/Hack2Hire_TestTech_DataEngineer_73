FROM python:3.11.5-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "weather_data.py"]
