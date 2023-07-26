import pandas as pd
import numpy as np
import datetime
import requests
from functions import get_deviations

def main():
    # global lat, lon
    startyear = int(input("Enter the start year(base): "))
    endyear = int(input("Enter the end year(base): "))
    lat=float(input("Enter the latitude: "))
    lon=float(input("Enter the longitude: "))
    
    print('\nANOMALY FOR 2023....\n')
    month = int(input("Enter the month (1-12): "))
    week = int(input("Enter the week (1-4): "))
    day = int(input("Enter the day (1-31): "))
    print("\nGETTING RESULTS....\n")
    monthdev, weekdev, daydev = get_deviations(startyear, endyear, lat, lon, month, week, day)

    print(f"MONTH Deviation for Month {month}: {monthdev:.2f}%")
    print(f"WEEK Deviation for Month {month}, Week {week}: {weekdev:.2f}%")
    print(f"DAY Deviation for Month {month}, Day {day}: {daydev:.2f}%")

if __name__ == "__main__":
    main()
