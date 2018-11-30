# shipwell_assessment

This repository contains my work for the Shipwell assessment.

The URL that will return the average temperature for a given lat / lon is as follows: 

`http://127.0.0.1:8000/weather/<lat>/<lon>/<site_filter_1>/<site_filter_2>`

The URL accepts 0-2 site filters.

Most of the relevant work is in two files: `assessment.weather.views.py` and `assessment.weather.urls.py`.
