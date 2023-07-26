import pandas as pd
import numpy as np
import datetime
import requests

def get_data(lat, lon,startyear,endyear):
    api=f'https://archive-api.open-meteo.com/v1/archive?latitude={lat:.2f}&longitude={lon:.2f}&start_date={startyear}-01-01&end_date={endyear}-12-31&hourly=shortwave_radiation'
    response=requests.get(api)
    if response.status_code==200:
        data=response.json()['hourly']
        columns = data.keys()
        column_data = {}
        for column in columns:
            column_data[column] = data[column]
        df = pd.DataFrame(column_data)
        df=df.rename(columns={'time':'Time'})
        return df.reset_index(drop=True)
    else:
        print("Failed to retrieve data from the API")
#df=get_data(lat, lon,startyear,endyear)
def get_monthly_data(month,lat,lon):
    month = str(month).zfill(2)
    api=f'https://archive-api.open-meteo.com/v1/archive?latitude={lat:.2f}&longitude={lon:.2f}&start_date=2023-{month}-01&end_date=2023-{month}-31&hourly=shortwave_radiation'
    response=requests.get(api)
    if response.status_code==200:
        data=response.json()['hourly']
        columns = data.keys()
        column_data = {}
        for column in columns:
            column_data[column] = data[column]
        df = pd.DataFrame(column_data)
        df=df.rename(columns={'time':'Time'})
        return df
    else:
        print("Failed to retrieve data from the API")

def all_month_avg(data):
    data['Time'] = pd.to_datetime(data['Time'])
    arr = []
    for i in range(1, 13):
        month_data = data[data['Time'].dt.month == i]
        if not month_data.empty:
            month_sum = month_data['shortwave_radiation'].sum()
            month_avg = month_sum / len(month_data)
            arr.append(month_avg)
        else:
            arr.append(0) 
    return arr

def all_month_weekly_avg(data):
    data['Time'] = pd.to_datetime(data['Time'])
    month_weekly_avgs = {}
    for i in range(1, 13):
        month_data = data[data['Time'].dt.month == i]
        if not month_data.empty:
            month_weekly_avgs[i] = []
            weeks = (month_data['Time'].dt.day-1) // 7 + 1
            for week in range(1, 5):  # Four weeks: 1-7, 8-14, 15-21, 22-31
                week_data = month_data[weeks == week]
                if not week_data.empty:
                    week_sum = week_data['shortwave_radiation'].sum()
                    week_avg = week_sum / len(week_data)
                    month_weekly_avgs[i].append(week_avg)
                else:
                    month_weekly_avgs[i].append(0)
        else:
            month_weekly_avgs[i] = [0] * 4
    return month_weekly_avgs

def all_month_daily_avg(df):
    month_daily_avgs = {}
    for i in range(1, 13):
        month_data = df[df['Time'].dt.month == i]
        if not month_data.empty:
            month_daily_avgs[i] = []
            days = month_data['Time'].dt.day
            for day in range(1, 32):
                day_data = month_data[days == day]
                if not day_data.empty:
                    day_sum = day_data['shortwave_radiation'].sum()
                    day_avg = day_sum / len(day_data)
                    month_daily_avgs[i].append(day_avg)
                else:
                    month_daily_avgs[i].append(0)
        else:
            month_daily_avgs[i] = [0] * 31
    return month_daily_avgs

def currmonthavg(month,lat, lon):
    df=get_monthly_data(month,lat,lon)
    if not df.empty:
        avg=df['shortwave_radiation'].mean()
        return avg
    else:
        return None          
            
def currweekavg(month, week,lat, lon):
    month_data = get_monthly_data(month, lat, lon)
    month_data['Time']=pd.to_datetime(month_data['Time'])
    if not month_data.empty:
        month_data['WeekNumber'] = (month_data['Time'].dt.day - 1) // 7 + 1
        week_data = month_data[month_data['WeekNumber'] == week]
        if not week_data.empty:
            week_avg = week_data['shortwave_radiation'].mean()
            return week_avg
        else:
            return 0
    else:
        return 0

def currdayavg(month,day,lat, lon):
    month_data=get_monthly_data(month, lat, lon)
    month_data['Time']=pd.to_datetime(month_data['Time'])
    if not month_data.empty:
        day_data=month_data[month_data['Time'].dt.day==day]
        if not day_data.empty:
            day_avg=day_data['shortwave_radiation'].mean()
            return day_avg
        else:
            return 0
    else:
        return 0
    
def monthdeviation(month,lat, lon):
    #month in integers
    curr_monthavg=currmonthavg(month,lat, lon)
    deviation1= ((curr_monthavg - monthlyavg1[month-1])/monthlyavg1[month-1])*100
    return deviation1
          
def weekdeviation(month,week,lat, lon):
    curr_weekavg=currweekavg(month, week,lat, lon)
    deviation1=((curr_weekavg - weeklyavg1[month][week-1])/weeklyavg1[month][week-1])*100
    return deviation1

def daydeviation(month,day,lat, lon):
    curr_dayavg=currdayavg(month, day,lat, lon)
    if (dailyavg1[month][day-1]!=0):
        deviation1=((curr_dayavg- dailyavg1[month][day-1])/dailyavg1[month][day-1])*100
        return deviation1
    else:
        return 0
# def get_location_coordinates(location_name):
#     location_coordinates = {
#         "charanka": (23.88, 71.18),
#         "rewa": (24.48, 81.61),
#         "goyalri": (27.95, 72.99),
#         "warangal": (17.50, 79.56),

#     }

    # if location_name in location_coordinates:
    #     return location_coordinates[location_name]
    # else:
    #     print(f"Location '{location_name}' not found.")
    #     return None
def get_deviations(startyear, endyear, lat, lon, month, week, day):
    global monthlyavg1, weeklyavg1, dailyavg1
    df1 = get_data(lat, lon, startyear, endyear)
    monthlyavg1 = all_month_avg(df1)
    weeklyavg1 = all_month_weekly_avg(df1)
    dailyavg1 = all_month_daily_avg(df1)

    monthdev = monthdeviation(month,lat, lon)
    weekdev = weekdeviation(month, week,lat, lon)
    daydev = daydeviation(month, day,lat, lon)

    return monthdev, weekdev, daydev
