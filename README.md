# Anomaly Detection Map

The Anomaly Detection Map is a Python project that analyzes Global Horizontal Irradiance (GHI) data from the Open Meteo API and detects anomalies in solar irradiance for specific locations and time periods.

## Features

- Retrieve GHI data for a specific location and time period
- Calculate monthly, weekly, and daily averages
- Calculate corresponding deviations and detect anomalies in solar irradiance(Only for data available till now)

## Requirements

- Python 3.7+

## Input
- Base Period(startyear and endyear)
- longitude
- lattitude
- Time to check the anomaly for particular location(month, week, day)

## Output
- Corresponding deviations from the base period
