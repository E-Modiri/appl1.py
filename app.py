

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔹 کلید API برای OpenWeatherMap (کلید شخصی خود را جایگزین کنید)
API_KEY = "a624c974a7c9d1161afac429a0011c35"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()

    # 🔹 دریافت نام شهر از Dialogflow
    city = req.get('queryResult', {}).get('parameters', {}).get('geo-city')

    if not city:
        return jsonify({"fulfillmentText": "I couldn't understand the city name. Please try again."})

    # 🔹 ارسال درخواست به OpenWeatherMap API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        result = f"The temperature in {city} is {temp}°C with {description}."
    else:
        result = "Sorry, I couldn't fetch the weather information."

    # 🔹 ارسال پاسخ به Dialogflow
    return jsonify({"fulfillmentText": result})


if __name__ == '__main__':
    app.run(port=5000)