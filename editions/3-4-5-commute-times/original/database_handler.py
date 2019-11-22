# -*- coding: utf-8 -*-
"""
Created on Sat June 29th 21:49 2019
@author: michael

This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)
"""


import os
import pandas as pd
import sqlite3



class Database():
    """
    Database is a class for handling database creation as well as adding and
    retrieving CommuteTime data.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        if not os.path.exists(db_path):
            print('Creating database: {}'.format(db_path))
            self.build_database()

    def build_database(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()

            cur.execute("CREATE TABLE CommuteTimes("
                        "Datetime DATE,"
                        "Origin TEXT,"
                        "Destination TEXT,"
                        "Distance INTEGER,"
                        "Summary TEXT,"
                        "Fastest REAL,"
                        "Slowest REAL,"
                        "Warnings TEXT"
                        ");")

    def add_data(self, data):
        """
        Add data to database. Expects a dictionary.
        """
        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO CommuteTimes values (?,?,?,?,?,?,?,?)",
                    (
                        data['Datetime'],
                        data['Origin'],
                        data['Destination'],
                        data['Distance'],
                        data['Summary'],
                        data['Fastest'],
                        data['Slowest'],
                        data['Warnings'],
                    )
                    )
        except Exception as e:
            print('Error writing data to database:', e)

    def get_data(self, start_date=None, end_date=None, specific_route=None):
        """
        Return data from database between start_date and end_date.
        Optionally allow a specific route: (origin, destination) tuple.
        Returns a pandas dataframe.
        """
        
        if specific_route:
            origin, destination = specific_route

        try:
            with sqlite3.connect(self.db_path) as con:  
                if specific_route:
                    if start_date:
                        if end_date:
                            # Start date and end date and specific route
                            query = "\
                            SELECT * FROM CommuteTimes \
                            WHERE (\
                            Datetime > ? AND \
                            Datetime < ? AND \
                            Origin = ? AND \
                            Destination = ? \
                            )"
                            params = (start_date, end_date, origin, destination,)
                        else:
                            # Start date only and specific route
                            query = "\
                            SELECT * FROM CommuteTimes \
                            WHERE (\
                            Datetime > ? AND \
                            Origin = ? AND \
                            Destination = ? \
                            )"
                            params = (start_date, origin, destination,)
                                                
                    elif end_date:
                        # End date only and specific route
                        query = "\
                            SELECT * FROM CommuteTimes \
                            WHERE (\
                            Datetime < ? AND \
                            Origin = ? AND \
                            Destination = ? \
                            )"
                        params=(end_date, origin, destination,)
    
                    else:
                        # No start or end date but specific route
                        query = "\
                            SELECT * FROM CommuteTimes \
                            WHERE (\
                            Origin = ? AND \
                            Destination = ? \
                            )"
                        params = (origin, destination,)

                else:
                    if start_date:
                        if end_date:
                            # Start date and end date
                            query = "SELECT * FROM CommuteTimes WHERE (Datetime > ? AND Datetime < ?)"
                            params = (start_date, end_date,)
                        else:
                            # Start date only
                            query = "SELECT * FROM CommuteTimes WHERE Datetime > ?"
                            params = (start_date,)
                                                
                    elif end_date:
                        # End date only
                        query = "SELECT * FROM CommuteTimes WHERE Datetime < ?"
                        params = (end_date,)
    
                    else:
                        # No start or end date
                        query = "SELECT * FROM CommuteTimes"
                        params = None
                    
                return pd.read_sql_query(query, con=con, parse_dates=['Datetime'], params=params)

        except Exception as e:
            print('Error getting data from database:', e)
