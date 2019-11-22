# -*- coding: utf-8 -*-
"""
Created on Sat June 29th 21:49 2019
@author: michael

This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)
"""

import datetime
import time

from commute_handler import get_commute_data
from database_handler import Database



def main(origins, destinations, api_key, database):
    """
    Iterate each combination of origin and destination and add commute data to database.
    """
    for origin in origins:
        for destination in destinations:
            if origin == destination: continue  # skip same origin and destination
            data = get_commute_data(origin, destination, api_key)
            database.add_data(data)


if __name__ == '__main__':

    HOME = '<home..>'
    WORK = '<work..>'

    API_KEY = '<api_key..>'
    DATABASE = Database(r'<database..>')

    while True:
        try:
            main(
                origins=[HOME, WORK],
                destinations=[WORK, HOME],
                api_key=API_KEY,
                database=DATABASE,
            )
            print('Getting commute data: [{}]'.format(datetime.datetime.now()))
        except Exception as e:
            print('Could not get data: [{}]'.format(datetime.datetime.now()), e)
        finally:
            time.sleep(1800)

    
        
