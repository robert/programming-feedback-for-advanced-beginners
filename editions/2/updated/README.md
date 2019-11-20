# Calculate Commute Times
Calculate commute times between arbitrary origins(s) and destination(s) using the Google Maps API, and write the data to a sqlite database.

Stores to the database:  
* Datetime stamp for commute calculation  
* The origin  
* The destination  
* The distance (in miles)  
* The route summary or main road name  
* The best-case (optimistic) commute time (in minutes)
* The worst-case (pessimistic) communte time (in minutes)
* Warnings (any accidents, construction zones, speed traps, etc..)


The Google Maps API allows for calculating hypothetical future commutes (specific times of day), but does not account for real-time events like accidents. Schedule this script with cron (Linux) or task scheduler (Windows), or just use time.sleep() in a while loop to pull the real-time data and store to a database to get a more realistic assesment of a typical commute.



This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)
