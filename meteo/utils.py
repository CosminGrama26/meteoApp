import requests
from datetime import datetime, timezone
from .models import Current_weather, Location, Update_tracker, Forecast

api_key = "4d71bcac975ee8a26882512838625119"


def update_hp():
    """Update weather for hp locations"""
    capitals = Location.objects.filter(is_county_seat=True)
    for location in capitals:
        # Make API call
        lat=location.latitude
        lon=location.longitude
        data = c_weather_api_call(lat, lon)
        if data == 1:
            continue
        # Delete old weather for location, if existent
        try:
            Current_weather.objects.get(location=location,  forecast__isnull=True).delete()
        except Current_weather.DoesNotExist:
            pass
        update_c_weather(location, data)

    Update_tracker.objects.get(name="hp_update").update()


def c_weather_api_call(lat, lon):
    """Make API call for current weather"""
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 1


def update_c_weather(location, data):
    """Update current_weather table"""

    # Extract data from JSON file
    main = data.get("weather")[0].get("main")
    icon_id = data.get("weather")[0].get("icon")
    temperature = data.get("main").get("temp")
    pressure = data.get("main").get("pressure")
    humidity = data.get("main").get("humidity")
    wind_speed = data.get("wind").get("speed")
    wind_direction = data.get("wind").get("deg")
    try:
        rain_1h = data.get("rain").get("1h")
    except AttributeError:
        rain_1h = 0
    try:
        snow_1h = data.get("snow").get("1h")
    except AttributeError:
        snow_1h = 0

    # Create and save new weather for location
    w = Current_weather(
        location=location,
        main=main,
        icon_id=icon_id,
        temperature=temperature,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        rain=rain_1h,
        snow=snow_1h
    )
    w.save()


def add_location(location):
    """Add input location to DB"""
    data = geo_api_call(location)

    # If location not found
    if data == 1:
        return 1
    
    # Extract data from JSON
    try:
        lat = data[0].get("lat")
        lon = data[0].get("lon")
    except IndexError:
        return 1
    
    #create and return new obj
    l = Location(
        name = location,
        latitude = lat,
        longitude = lon
    )
    l.save()
    return l


def geo_api_call(location):
    """Make geocode call"""
    country = "ITA"
    limit = 1
    api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location},{country}&limit={limit}&appid={api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 1
    

def update_location_weather(location):
    """Update location weather"""
    #Check if location has weather data;
    try:
        cw_old = Current_weather.objects.get(location=location,  forecast__isnull=True)
        t_delta = (datetime.now(timezone.utc) - cw_old.timestamp).total_seconds() / 60
        # If weather was update less than 1h ago, we return that update
        if t_delta < 60:
            return cw_old
        else:
            cw_old.delete()
    except Current_weather.DoesNotExist:
        pass

    # Add weather do DB
    lat = location.latitude
    lon = location.longitude
    data = c_weather_api_call(lat, lon)
    if data == 1:
        return 1
    update_c_weather(location, data)

    return Current_weather.objects.get(location=location,  forecast__isnull=True)


def update_location_forecast(location):
    """Update location forecast"""
    #Check if location has forecast data
    try:
        fc_old = Forecast.objects.filter(location=location)
        t_delta = (datetime.now(timezone.utc) - fc_old[0].timestamp).total_seconds() / 60
        if t_delta < 60:
            return fc_old
        else:
            for fc in fc_old:
                fc.delete()
    except Forecast.DoesNotExist:
        pass
    except IndexError:
        pass

    # Fetch forecast data
    lat = location.latitude
    lon = location.longitude
    data = forecast_api_call(lat, lon)
    if data == 1:
        return 1
    
    # Add forecast to db
    forecasts = []
    for forecast in data.get("list"):
        forecasts.append(add_forecast(location, forecast))
    
    return forecasts


def forecast_api_call(lat, lon):
    """Make API call for current forecast"""
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&cnt=24"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 1
    

def add_forecast(location, json_forecast):
    """add forecast to db"""
    # Extract data
    f_datetime = datetime.fromtimestamp(json_forecast.get("dt"), tz=timezone.utc)
    main = json_forecast.get("weather")[0].get("main")
    icon_id = json_forecast.get("weather")[0].get("icon")
    temperature = json_forecast.get("main").get("temp")
    pressure = json_forecast.get("main").get("pressure")
    humidity = json_forecast.get("main").get("humidity")
    wind_speed = json_forecast.get("wind").get("speed")
    wind_direction = json_forecast.get("wind").get("deg")
    try:
        rain_3h = json_forecast.get("rain").get("3h")
    except AttributeError:
        rain_3h = 0
    try:
        snow_3h = json_forecast.get("snow").get("3h")
    except AttributeError:
        snow_3h = 0

    # Create new object, save and return it
    fc = Forecast(
        f_datetime=f_datetime,
        location=location,
        main=main,
        icon_id=icon_id,
        temperature=temperature,
        pressure=pressure,
        humidity=humidity,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        f_rain=rain_3h,
        f_snow=snow_3h
    )
    fc.save()
    return fc