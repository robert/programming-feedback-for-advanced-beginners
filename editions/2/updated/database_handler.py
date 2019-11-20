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

    def build(self):
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

    def get_data(self, start_date=None, end_date=None, specific_route=None):
        """
        Return data from database between start_date and end_date.
        Optionally allow a specific route: (origin, destination) tuple.
        Returns a pandas dataframe.
        """
        
        if specific_route:
            origin, destination = specific_route

        filters = []
        if specific_route:
            filters.append(("Origin = ?", origin))
            filters.append(("Destination = ?", destination))

        if start_date:
            filters.append(("Datetime > ?", start_date))

        if end_date:
            filters.append(("Datetime < ?", end_date))

        query = "SELECT * FROM CommuteTimes "
        if len(filters) > 0:
            # l = [f[0] for f in filters] is a Python "list comprehension". It
            # is shorthand for:
            #
            #   l = []
            #   for f in filters:
            #       l.append(f[0])
            query += " WHERE " + " AND ".join([f[0] for f in filters])
            
        with sqlite3.connect(self.db_path) as con:  
            return pd.read_sql_query(query, con=con, parse_dates=['Datetime'], params=[f[1] for f in filters])
