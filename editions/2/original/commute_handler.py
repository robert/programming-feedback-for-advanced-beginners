# -*- coding: utf-8 -*-
"""
Created on Sat June 29th 21:49 2019
@author: michael

This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)
"""


from datetime import datetime
import googlemaps


def get_commute_data(origin, destination, api_key):
    """
    Get the current (real-time) drive time data (best and worst case) 
    between <origin> and <destination> using google maps API.
    
    Returns a dictionary with:
    * the route summary (main road or route name),
    * the distance (in miles), 
    * the best case (in minutes),
    * the worst case (in minutes),
    * and any warnings (accidents etc).

    Requires a google maps API Key.
    """

    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()

    best_case = gmaps.directions(
            origin, destination, mode='driving', traffic_model='optimistic', departure_time=now)[0]
    worst_case = gmaps.directions(
            origin, destination, mode='driving', traffic_model='pessimistic', departure_time=now)[0]

    commute_data = {
        'Datetime'   : now,
        'Origin'     : origin,
        'Destination': destination,
        'Distance'   : round(best_case['legs'][0]['distance']['value'] * 0.000621371, 1), # In miles
        'Summary'    : best_case['summary'],  # Main road or route name 
        'Fastest'    : round(best_case['legs'][0]['duration_in_traffic']['value']/60.0, 1),  # In minutes
        'Slowest'    : round(worst_case['legs'][0]['duration_in_traffic']['value']/60.0, 1),  # In minutes
        'Warnings'   : ', '.join(best_case['warnings']),  # Accidents, construction, and speed traps
        }
    return commute_data
