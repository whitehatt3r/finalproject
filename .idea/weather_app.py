import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
from datetime import datetime

def get_weather():
    city = city_entry.get()
    api_key_weather = '9b78e42ab603def4cac1082119cbf3c5'  # OpenWeatherMap API key
    api_key_maps = 'AIzaSyCcxwkQ0TuL0GeKAFtvBAwJdy7CrIyMZGo'  # Google Maps API key

    # Fetch current weather data
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},US&appid={api_key_weather}&units=metric"
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        update_current_weather(weather_data, api_key_maps)
    else:
        result_label.config(text="Failed to retrieve weather data. Please check the city name.")

    # Fetch forecast data
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},US&appid={api_key_weather}&units=metric"
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        update_forecast(forecast_data)
    else:
        forecast_label.config(text="Failed to retrieve forecast data.")

def update_current_weather(weather_data, api_key_maps):
    # Extract data
    city_name = weather_data['name'] + ', ' + weather_data['sys']['country']
    temp_c = weather_data['main']['temp']
    temp_f = temp_c * 9 / 5 + 32  # Convert Celsius to Fahrenheit for Us Americans :)
    weather_desc = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    pressure = weather_data['main']['pressure']
    clouds = weather_data['clouds']['all']

    # Display weather info
    weather_info = f"Weather in {city_name}:\n"
    weather_info += f"Temperature: {temp_c}°C / {temp_f:.1f}°F\n"
    weather_info += f"Conditions: {weather_desc}\n"
    weather_info += f"Humidity: {humidity}%\n"
    weather_info += f"Wind Speed: {wind_speed} m/s\n"
    weather_info += f"Pressure: {pressure} hPa\n"
    weather_info += f"Cloudiness: {clouds}%"
    result_label.config(text=weather_info)

    # Load and display static map using Google Maps Static API
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=10&size=450x450&maptype=roadmap&key={api_key_maps}"
    map_response = requests.get(map_url)
    if map_response.status_code == 200:
        map_image = Image.open(io.BytesIO(map_response.content))
        map_photo = ImageTk.PhotoImage(map_image)
        map_label.config(image=map_photo)
        map_label.image = map_photo  # keep a reference!

def update_forecast(forecast_data):
    forecast_text = "5 Day Forecast:\n"
    for item in forecast_data['list'][:40:8]:  # Displaying only 5 days, every 24 hours
        dt = datetime.fromtimestamp(item['dt'])
        temp_c = item['main']['temp']
        temp_f = temp_c * 9 / 5 + 32
        forecast_text += f"{dt.strftime('%a, %b %d')} - Temp: {temp_c}°C / {temp_f:.1f}°F ({item['weather'][0]['description']})\n"
    forecast_label.config(text=forecast_text)

app = tk.Tk()
app.title("Weather App")

tab_control = ttk.Notebook(app)

# Current Weather Tab
weather_tab = ttk.Frame(tab_control)
tab_control.add(weather_tab, text='Current Weather')
tab_control.pack(expand=1, fill='both')

tk.Label(weather_tab, text="Enter City or ZIP code:").pack()
city_entry = tk.Entry(weather_tab)
city_entry.pack()
tk.Button(weather_tab, text="Get Weather", command=get_weather).pack()
result_label = tk.Label(weather_tab, text="")
result_label.pack()
map_label = tk.Label(weather_tab)
map_label.pack()

# Forecast Tab
forecast_tab = ttk.Frame(tab_control)
tab_control.add(forecast_tab, text='Forecast')
forecast_label = tk.Label(forecast_tab, text="")
forecast_label.pack()

app.mainloop()
