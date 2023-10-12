from flask import Flask, render_template
from datetime import datetime, timedelta
import requests

# Constants
PRAYER_TIMES_API_URL = "http://www.islamicfinder.us/index.php/api/prayer_times"

def get_public_ip() -> str:
    """Retrieve the public IP of the user."""
    # return requests.get("https://ifconfig.me").text
    return "213.158.188.59"

def get_prayer_times(user_ip: str) -> dict:
    """Fetch prayer times based on the user's IP."""
    params = {"user_ip": user_ip, "method": "5"}
    response = requests.get(PRAYER_TIMES_API_URL, params=params)
    return response.json()["results"]

def convert_to_datetime(time_str: str) -> datetime:
    """Convert a 12-hour formatted string to a datetime object."""
    formatted_time_str = time_str.replace('%', '')
    return datetime.strptime(formatted_time_str, '%I:%M %p')

def calculate_last_third_of_night(maghrib: datetime, fajr: datetime) -> (datetime, datetime):
    """Calculate the start time of the last third of the night."""
    if fajr < maghrib:
        fajr += timedelta(days=1)
    night_duration = fajr - maghrib
    one_third_duration = night_duration / 3
    last_third_start = maghrib + 2 * one_third_duration
    return last_third_start, fajr

app = Flask(__name__)

@app.route('/')
def index():
    user_ip = get_public_ip()
    prayer_times = get_prayer_times(user_ip)
    maghrib_time = convert_to_datetime(prayer_times['Maghrib'])
    fajr_time = convert_to_datetime(prayer_times['Fajr'])
    last_third_start_time, _ = calculate_last_third_of_night(maghrib_time, fajr_time)

    return render_template('index.html', 
                           last_third_start_time=last_third_start_time.strftime('%I:%M %p'),
                           fajr_time=fajr_time.strftime('%I:%M %p'))

if __name__ == '__main__':
    app.run(debug=True)
