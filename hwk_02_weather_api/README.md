# Homework 02

## Open Weather API

## Goal

To illustrate how to use an API to collect weather-related data. 

## Instructions 

In this assignment you are asked to register a free account on [https://openweathermap.org/](https://openweathermap.org/). Then study the API's documentation to extract weather info from locations described in data/locations.csv. Your program should save the collected info in JSON format, similar to: 

```
[
    {"today": "2021-09-01 14:41:32", "city": "Denver", "state": "CO", "temp_min": 80, "temp_max": 91, "temp": 86}, 
    {"today": "2021-09-01 14:41:32", "city": "Colorado Springs", "state": "CO", "temp_min": 70, "temp_max": 89, "temp": 82}, 
    {"today": "2021-09-01 14:41:32", "city": "Aspen", "state": "CO", "temp_min": 54, "temp_max": 73, "temp": 64}, 
    {"today": "2021-09-01 14:41:32", "city": "Phoenix", "state": "AR", "temp_min": 86, "temp_max": 94, "temp": 90}, 
    {"today": "2021-09-01 14:41:32", "city": "Tucson", "state": "AR", "temp_min": 80, "temp_max": 89, "temp": 85},
    {"today": "2021-09-01 14:41:32", "city": "Los Angeles", "state": "CA", "temp_min": 67, "temp_max": 85, "temp": 73}, 
    {"today": "2021-09-01 14:41:32", "city": "Bethlehem", "state": "PA", "temp_min": 64, "temp_max": 72, "temp": 66}, 
    {"today": "2021-09-01 14:41:32", "city": "Miami", "state": "FL", "temp_min": 86, "temp_max": 96, "temp": 91}, 
    {"today": "2021-09-01 14:41:32", "city": "Boston", "state": "MA", "temp_min": 64, "temp_max": 69, "temp": 66}
]
```
