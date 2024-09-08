import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Constants
API_KEY = '1a5ff14a57bd16f7c216a107f63bc1a3'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
HISTORICAL_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to fetch current weather data
def fetch_current_weather(city_name):
    try:
        response = requests.get(BASE_URL, params={
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'  # Temperature in Celsius
        })
        response.raise_for_status()  #Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to fetch historical weather data
def fetch_historical_weather(city_name, date):
    try:
        # Convert date to Unix timestamp
        timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
        response = requests.get(HISTORICAL_BASE_URL, params={
            'lat': 0,  # Replace with actual latitude
            'lon': 0,  # Replace with actual longitude
            'dt': timestamp,
            'appid': API_KEY,
            'units': 'metric'
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return None

# Function to calculate statistics
def calculate_statistics(temperatures):
    stats = {
        'average': np.mean(temperatures),
        'median': np.median(temperatures),
        'mode': float(pd.Series(temperatures).mode())
    }
    return stats

# Function to save data to a file
def save_to_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

# Function to process and format the weather data
def process_weather_data(weather_data):
    if weather_data:
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"The current temperature is {temperature}°C with {description}."
    return "No weather data available."

# Function to handle user input
def get_user_input():
    while True:
        city_name = input("Enter the name of the city: ").strip() 
        if city_name:
            return city_name
        print("City name cannot be empty. Please try again.")

# Main function
def main():
    city_name = get_user_input()
    
    # Fetch current weather data
    current_weather = fetch_current_weather(city_name)
    print(process_weather_data(current_weather))
    
    # Fetch historical weather data
    date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")  
    historical_weather = fetch_historical_weather(city_name, date)
    
    # Process historical data
    if historical_weather and 'hourly' in historical_weather:
        temperatures = [hour['temp'] for hour in historical_weather['hourly']]
        stats = calculate_statistics(temperatures)
        print(f"Statistics for {date}:")
        print(f"Average Temperature: {stats['average']}°C")
        print(f"Median Temperature: {stats['median']}°C")
        print(f"Mode Temperature: {stats['mode']}°C")
        
        # Save results to a file
        data = {
            'current_weather': current_weather,
            'historical_weather': historical_weather,
            'statistics': stats
        }
        save_to_file('weather_data.json', data)

if __name__ == "__main__":
    main()
