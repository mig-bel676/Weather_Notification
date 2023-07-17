import os

import requests
# Messaging API
from twilio.rest import Client

# Authorization for using Twilio Messaging API
account_sid = os.environ.get('account_sid')
auth_token = os.environ.get('auth_token')


degree_sign = u'\N{DEGREE SIGN}'
# Weather API Endpoint
Weather_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
# Configure latitude and longitude for weather for targeted area
weather_parameters = {
    "lat": 33.916069,
    "lon": -118.155472,
    "appid": '31e391c2c76b8e68ece77449c717ffa4',
    "units": 'imperial'
}

# Weather API request
response = requests.get(Weather_Endpoint, params=weather_parameters)
response.raise_for_status()
data = response.json()
hourly_weather_list = [data["hourly"][hour]["weather"][0]["id"] for hour in range(12)]
# Data retrieved by Weather API
print(data)

# Gathers data from JSON to retrieve the highest temp for the day  temp for the day
max_Temp = data["daily"][0]["temp"]["max"]
print(max_Temp)
weather_checker = []
for weather in hourly_weather_list:
    # Convert Weather API data into readable data for recipient
    if weather < 700:
        weather_checker.append("Rain")
    else:
        weather_checker.append("Clear")
print(weather_checker)


# Sends a SMS to reciepient that has tailored message based on Weather API
if "Rain" in weather_checker:
    client = Client(account_sid, auth_token)
    percent_rain = data["daily"][0]["pop"]
    message = client.messages.create(body=f"Today is {max_Temp}{degree_sign} "
                                          f"There's a {percent_rain * 100}% chance that it is"
                                          f" going to rain later. Umbrella time ☔️",
                                     from_='+15737314325', to='5624450411' # Recipient Phone Number
                                     )
    print(message.sid)
elif "Cloud" in weather_checker:
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=f"Today is {max_Temp}{degree_sign} "
                                          f"Pretty cloudy today, enjoy the clouds 🌥️",
                                     from_='+15737314325', to='5624450411' # Recipient Phone Number
                                     )
    print(message.sid)

else:
    client = Client(account_sid, auth_token)
    percent_rain = data["daily"][0]["pop"]
    message = client.messages.create(body=f"Today is {max_Temp}{degree_sign} "
                                          f"Clear skies, enjoy the sun ☀️",
                                     from_='+15737314325', to='5624450411' # Recipient Phone Number
                                     )
    print(message.sid)