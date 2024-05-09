# MY METEO APP

By Florin Cosmin Grama

### Video Demo: <https://youtu.be/xF_FQRHBP1E>

## Description

This web app realised with Django and JS provides updated weather and forecast data for Italy. Regional capitals are highlighted on a map in the homepage, but the user is able to search for any location in Italy. Logged users can also add various locations to their favorites. The web app is responsive to the window dimensions.

To run the application, it suffices to run the command `python3 manage.py runserver` and access the server link within a web browser.

Data is provided by <http://openweathermap.org> and it is accessed through their API service.

## Project components
The project is composed of multiple files.
### Django back-end files
- `models.py`, which contains the following models:
    - `User`: it is a Subclass of the AbstractUser class, and it keeps track of registered users.
    - `Update_tracker`: a model used for keeping track of the last update of the homepage.
    - `Location`: saves data regarding already searched locations, i.e. latitude, longitude, and name. Regional capitals, displayed in the homepage, also have the `is_county_seat` field set as `True`.
    - `Current_weather`: saves real-time weather data regarding a location.
    - `Forecast`: a subclass of the `Current_weather` model, it also stores the datetime to which the forecast is referring to. Additionally, rain and snow quantity fields have different validators compared to the parent class.
    - `Favorite`: stores user's favorite location by matching a `User` model with a `Location` model, as foreign keys.
- `views.py`, which contains the following views:
    - `index`: loads weather data of the regional capitals and displays it on the homepage. It also ensures that this data is not refreshed more often than every 60 minutes, regardless of the user.
    - `location`: loads weather and forecast for a specific location and renders it on the `meteo/location.html` template.
    - `check_favorite`: in case of `GET` request, it checks if a location is among user's favorites; in case of `PUT` request, add or removes a favorite from a user's favorite list.
    - `favorites`: loads user's favorite locations.
    - `login_view`: logs in the user.
    - `logout_view`: logs out the user.
    - `register`: registers the user.
- `utils.py`, which contains helper functions for `views.py`, such as:
    - `update_hp`: updates current weather for all homepage locations, deletes older data and updates the `Update_tracker`
    - `c_weather_api_call`: makes API call for current weather of a location. It accepts as arguments latitude and longitude of said location.
    - `update_c_weather`: creates and saves new `Current_weather` object.
    - `add_location`: provided with the name of a location, creates, and saves a new `Location` object.
    - `geo_api_call`: provided with the name of a location, makes the API call that return location's coordinates.
    - `update_location_weather`: updates weather of a specific location, but only if it was not updated in the last 60 minutes. If older data exists for said location, it will be deleted. 
    - `update_location_forecast`: updates forecasts of a specific location, but only if it was not updated in the last 60 minutes. If older data exists for said location, it will be deleted.
    - `forecats_api_call`: makes API call for weather forecast of a location. It accepts as arguments latitude and longitude of said location.
    - `add_forecast`: creates and saves new `Forecast` object.
- `templatetags/meteo_extras.py`: contains Jinja filters used in the Django templates:
    - `round_int`: returns the rounded value of a number. Used for temperature.
    - `weekday`: given a timestamp, it returns in a format such as "Monday 21:00".
    - `ms_to_kmh`: converts ms/s into km/h. Used for wind speed.
    - `deg_to_card`: converts degrees to cardinal directions. Used for wind direction.
### Django HTML templates
- `layout.html`: Contains all the `<head>` data, including links to stylesheets, scripts, and some global JS variables. It also contains the navbar and the footer. All other templates expand this one.
- `index.html`: it is the homepage; it contains a map with icons representing the weather of the regional capitals. Those icons are clickable. Icons are positioned on the map with help of the `styles.css` file.
- `location.html`: displays current weather and forecast for a specific location. 
- `favorites.html`: displays a list of user's favorite locations, with brief weather description. List elements are clickable.
- `login.html`: login page.
- `register.html`: register page.
- `error.html`: page used to display error messages.

### JavaScript front-end
The front-end of the app is managed by the file `index.js`, which contains the following functions:
- `addSearchBar`: adds a search bar after the DOM is loaded. When the submit button ins clicked, redirects to the searched location url.
- `lightNavBar`: Sets the current page as `active` on the navbar
- `manageFavorites`: This function is executed if an authenticated user is on a `location` page. Sends `PUT` request to the `check_favorite` view in order to add/remove the location from user's favorites.
- `updateButton`: called by `manageFavorites`, this async function updates the class and the innerHTML of the favorite button after the DOM is loaded and after every click on the button. It achieves that by sending a `GET` request to the `check_favorite` view. 
- `addLocationLink`: executed in the `favorites` page, makes each location of the list clickable, and redirects to the respective `location` page.
