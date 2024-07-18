from geopy.geocoders import Nominatim
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u
from datetime import datetime

from datetime import datetime
from geopy.geocoders import Nominatim
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
import astropy.units as u


def get_zenith_ra_dec(date_str, time_str, location_str):
    # Initialize geolocator
    geolocator = Nominatim(user_agent="zenith_locator")
    
    # Get location coordinates
    location = geolocator.geocode(location_str)
    if location is None:
        return "Location not found."
    
    latitude = location.latitude
    longitude = location.longitude
    
    # Try to parse the date using different formats
    date_formats = ["%d-%m-%Y", "%Y-%m-%d"]
    date_obj = None
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue
    
    if date_obj is None:
        return "Invalid date format. Please use DD-MM-YYYY or YYYY-MM-DD."
    
    date_iso_str = date_obj.strftime("%Y-%m-%d")
    
    # Combine date and time into a single time object
    datetime_str = f"{date_iso_str}T{time_str}"
    observation_time = Time(datetime_str)

    # Define the observer's location
    observer_location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg)

    # Define the AltAz frame
    altaz = AltAz(obstime=observation_time, location=observer_location)

    # Zenith point is at 90 degrees altitude
    zenith_altaz = SkyCoord(alt=90*u.deg, az=0*u.deg, frame=altaz)
    
    # Transform to ICRS (RA, Dec)
    zenith_icrs = zenith_altaz.transform_to('icrs')
    
    zenith_ra = zenith_icrs.ra.deg
    zenith_dec = zenith_icrs.dec.deg
    
    return zenith_ra, zenith_dec

