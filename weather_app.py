import requests
import json
import time

API_KEY = "a19de98d6776401fa10112907240101"
BASE_URL = "http://api.weatherapi.com/v1"
FAVORITES_FILE = "favorites.json"

def get_weather_by_city(city):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: Unable to fetch weather data for {city}. Status code: {response.status_code}")
        return None

def display_weather(weather_data):
    if weather_data:
        print("\nCurrent Weather:")
        location = weather_data['location']
        current_weather = weather_data['current']
        print(f"Location: {location['name']}, {location['region']}, {location['country']}")
        print(f"Temperature: {current_weather['temp_c']}°C")
        print(f"Condition: {current_weather['condition']['text']}")
    else:
        print("Unable to display weather information.")

def add_favorite(city):
    favorites = get_favorites()

    if city not in favorites:
        favorites.append(city)
        save_favorites(favorites)
        print(f"{city} added to favorites.")
    else:
        print(f"{city} is already in favorites.")

def remove_favorite(city):
    favorites = get_favorites()

    if city in favorites:
        favorites.remove(city)
        save_favorites(favorites)
        print(f"{city} removed from favorites.")
    else:
        print(f"{city} is not in favorites.")

def list_favorites():
    favorites = get_favorites()
    print("\nFavorites:")
    for city in favorites:
        print(city)

def get_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as file:
            favorites = json.load(file)
    except FileNotFoundError:
        favorites = []
    return favorites

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as file:
        json.dump(favorites, file)

def main():
    try:
        while True:
            print("\nOptions:")
            print("1. Check weather by city name")
            print("2. Add favorite city")
            print("3. Remove favorite city")
            print("4. List favorite cities")
            print("5. Auto-refresh weather for a city")
            print("6. Quit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                city_name = input("Enter the city name: ")
                weather_data = get_weather_by_city(city_name)
                display_weather(weather_data)
            elif choice == '2':
                city_name = input("Enter the city name to add to favorites: ")
                add_favorite(city_name)
            elif choice == '3':
                city_name = input("Enter the city name to remove from favorites: ")
                remove_favorite(city_name)
            elif choice == '4':
                list_favorites()
            elif choice == '5':
                city_name = input("Enter the city name for auto-refresh: ")
                while True:
                    weather_data = get_weather_by_city(city_name)
                    display_weather(weather_data)
                    time.sleep(15)  # Auto-refresh every 15 seconds
            elif choice == '6':
                print("Exiting the weather application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting gracefully.")


if __name__ == "__main__":
    main()

