# -*- coding: utf-8 -*-
"""
Created on Sat June 29th 21:49 2019
@author: michael

This code is made available under the Creative Commons Zero 1.0 License (https://creativecommons.org/publicdomain/zero/1.0)
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot_data(data, route_name=''):
    times = pd.to_datetime(data.Datetime)
    
    optimistic_mean = data.groupby([times.dt.hour]).Fastest.mean()
    optimistic_std = data.groupby([times.dt.hour]).Fastest.std()
    optimistic_min = data.groupby([times.dt.hour]).Fastest.min()
    optimistic_max = data.groupby([times.dt.hour]).Fastest.max()
    
    pessimistic_mean = data.groupby([times.dt.hour]).Slowest.mean()
    pessimistic_std = data.groupby([times.dt.hour]).Slowest.std()
    pessimistic_min = data.groupby([times.dt.hour]).Slowest.min()
    pessimistic_max = data.groupby([times.dt.hour]).Slowest.max()
        
    average_case = (optimistic_mean + pessimistic_mean) / 2
    
    xs = optimistic_mean.index
       
    plt.figure(figsize=(12,8))
    
    plt.plot(xs, optimistic_mean, c='b', label='Optimistic Estimate')
    plt.errorbar(
            xs,
            optimistic_mean,
            optimistic_std,
            ls='',
            c='b',
            alpha=0.2,
            label='Optimistoc Std Dev'
            )
    plt.fill_between(
            xs,
            optimistic_min,
            optimistic_max,
            color='b',
            alpha=0.15,
            label='Optimistic Range'
            )
    
    plt.plot(xs, pessimistic_mean, c='r', label='Pessimistic Estimate')
    plt.errorbar(
            xs,
            pessimistic_mean,
            pessimistic_std,
            ls='',
            c='r',
            alpha=0.2,
            label='Pessimistic Std Dev'
            )
    plt.fill_between(
            xs,
            pessimistic_min,
            pessimistic_max,
            color='r',
            alpha=0.15,
            label='Pessimistic Range'
            )
    plt.plot(xs, average_case, c='black', alpha=0.5, label='Average Estimate')
    
    plt.title('Average Commute Times\n{}'.format(route_name), fontsize=16)
    plt.ylabel('Minutes', fontsize=16)   
    plt.xlabel('Hour of Day', fontsize=16)
    
    plt.xticks(xs)
    plt.legend()
    
    plt.show()
    
        

def main(database, start_date=None, end_date=None, specific_route=None):
    data = database.get_data(start_date=start_date, end_date=end_date, specific_route=specific_route)
    name = 'From: {}\nTo: {}'.format(*specific_route)
    plot_data(data, route_name=name)
    
