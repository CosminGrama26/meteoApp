from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Location, Current_weather, Update_tracker, Favorite
from .utils import update_hp, add_location, update_location_weather, update_location_forecast

# Create your views here.
def index(request):
    """Loads current weather"""
    # GET method required
    if request.method != "GET":
        return render(request, "meteo/error.html", {
            "message":"GET method required"
        })

    # Check time elapsed since last hp update
    last_hp_update = Update_tracker.objects.get(name='hp_update').last_updated
    t_delta = (datetime.now(timezone.utc) - last_hp_update).total_seconds() / 60
    
    if t_delta > 60:
        update_hp()

    # Load data from db
    weathers = []
    capitals = Location.objects.filter(is_county_seat=True)
    for location in capitals:
        try:
            weather = Current_weather.objects.get(location=location, forecast__isnull=True)
        except Current_weather.DoesNotExist:
            continue
        weather.location = location
        weathers.append(weather)

    return render(request, "meteo/index.html", {
        "weathers": weathers
    })


def location(request, location):
    """Loads weather and forecast for a specific location"""
    # GET method required
    if request.method != "GET":
        return render(request, "meteo/error.html", {
            "message":"GET method required"
        })

    # Check if location is in DB; if not, try to add
    location = location.capitalize()
    try:
        location_o = Location.objects.get(name=location)
    except Location.DoesNotExist:
        location_o = add_location(location)
        if location_o == 1:
            return render(request, "meteo/error.html", {
                "message":"Location not found."
            })
    
    # Update wheather for location, if necessary
    weather = update_location_weather(location_o)
    forecasts = update_location_forecast(location_o)

    if weather == 1 or forecasts == 1:
        return render(request, "meteo/error.html", {
                "message":"Error while fetching data."
            })
    
    return render(request, "meteo/location.html", {
        "location":location, "weather": weather,
        "forecasts":forecasts
    })


@login_required(login_url="login")
def check_favorite(request, location):
    """Check if location is among user's favorites
    Toggle add/remove favorite"""

    #Identify location
    location = location.capitalize()
    try:
        location_o = Location.objects.get(name=location)
    except Location.DoesNotExist:
        return render(request, "meteo/error.html", {
                "message":"Location not found."
            })
    
    # GET returns 1 if favorite, 0 if not
    if request.method == "GET":
        try:
            Favorite.objects.get(user=request.user, location=location_o)
        except Favorite.DoesNotExist:
            return JsonResponse({"favorite": 0}, status=200)
        return JsonResponse({"favorite": 1}, status=200)
    
    # PUT request adds/removes favorite
    elif request.method == "PUT":
        try:
            f = Favorite.objects.get(user=request.user, location=location_o)
            f.delete()
            return JsonResponse({"action": "deleted"}, status=201)
        except Favorite.DoesNotExist:
            f = Favorite(user=request.user, location=location_o)
            f.save()
            return JsonResponse({"action": "added"}, status=201)

    # Request must be GET or PUT
    else:
        return render(request, "meteo/error.html", {
            "message":"GET or PUT method required"
        })


@login_required(login_url="login")
def favorites(request):
    """Loads user's favorite locations"""
    # GET method required
    if request.method != "GET":
        return render(request, "meteo/error.html", {
            "message":"GET method required"
        })
    
    # Filter favorite locations
    locations = []
    fav_locations = request.user.favorites.all()
    for fav_location in fav_locations:
        location_o = Location.objects.get(is_favorite=fav_location)
        location_w = update_location_weather(location_o)
        locations.append((location_o, location_w))

    return render(request, "meteo/favorites.html", 
        {"locations": locations})


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "meteo/login.html",
                {"message": "Invalid credentials."}
            )
    else:
        return render(request, "meteo/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "meteo/register.html",
                {"message": "Passwords must match."}
            )
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "meteo/register.html",
                {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "meteo/register.html")