from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
import board
import busio
import adafruit_bmp3xx
import requests
import datetime
import json

def get_average_value() -> float:
    timestamp = int((datetime.datetime.now() - datetime.timedelta(minutes=1000)).timestamp())
    url = f"http://localhost:8000/api/get/average?timestamp={timestamp}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data["average"]
    else:
        return None

def send_sensor_data(update: Update, context: CallbackContext) -> None:
    average = get_average_value()

    if average is None:
        message = "Датчик отсутствует"
    else:
        message = f"Температура и влажность : {average}"

app = ApplicationBuilder().token('6674261432:AAFPS6scUMQjK6eFU7W396QJMwWRZTv066E')

app.add_handler(CommandHandler('sensor', send_sensor_data))

app.run_polling()