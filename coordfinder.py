import math
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

def get_lat_lon(place_name):
    geolocator = Nominatim(user_agent="your_app_name")  # Replace "your_app_name" with your own user agent

    location = geolocator.geocode(place_name)
    
    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        print(f"Location not found for: {place_name}")
        return None

def calculate_zenith_coordinates(latitude, longitude, date, time):
    # Convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calculate the observer's altitude (in degrees)
    altitude = 90.0  # Assuming sea level for simplicity

    # Convert date and time to a datetime object
    datetime_str = f"{date} {time}"
    observation_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

    # Calculate the Julian Day
    julian_day = (observation_time - datetime(2000, 1, 1, 12, 0, 0)).days + 2451545.0

    # Calculate the observer's local sidereal time (LST)
    sidereal_time = (280.46061837 + 360.98564736629 * (julian_day - 2451545.0)
                     + lon_rad) % 360.0

    # Calculate the hour angle (in degrees)
    hour_angle = sidereal_time - 180.0

    # Convert angles to radians
    altitude_rad = math.radians(altitude)
    hour_angle_rad = math.radians(hour_angle)

    # Calculate the declination of the zenith point (in radians)
    declination_rad = math.asin(math.sin(lat_rad) * math.sin(altitude_rad)
                                + math.cos(lat_rad) * math.cos(altitude_rad) * math.cos(hour_angle_rad))

    # Calculate the right ascension of the zenith point (in radians)
    right_ascension_rad = math.atan2(math.sin(hour_angle_rad),
                                     math.cos(lat_rad) * math.tan(declination_rad)
                                     - math.sin(lat_rad) * math.cos(hour_angle_rad))

    # Convert angles back to degrees
    declination = math.degrees(declination_rad)
    right_ascension = math.degrees(right_ascension_rad)

    return right_ascension, declination