from django import template

register = template.Library()

def round_int(value):
    return round(value)


def weekday(timestamp):
    day = timestamp.strftime("%A %H:%M")
    return day


def ms_to_kmh(value):
    kmh = float(value) * 3.6
    return round(kmh)


def deg_to_card(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index_n = round(degrees / (360 / len(directions)))
    return directions[index_n % len(directions)]


register.filter("round_int", round_int)
register.filter("weekday", weekday)
register.filter("ms_to_kmh", ms_to_kmh)
register.filter("deg_to_card", deg_to_card)
    