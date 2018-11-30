from django.http import HttpResponse, JsonResponse

import requests


def weather(request, lat=None, lon=None, **kwargs):
    """
    Method to find the mean temperature at a given location. Has support for NOAA, Accuweather, and Weather.com.
    Has support to filter to any subset of these three sources.

    Args:
        request:            Standard initial argument for a Django view.
        lat:                Latitude of desired location.
        lon:                Longitude of desired location.
        kwargs:             List of subset of sources we want to use to calculate the average temperature.

    Returns:
        HTTP Response giving the average temperature of the desired location.
    """

    def mean(temperatures):
        """
        Calculate the mean of multiple temperatures.

        Args:
            temperatures:       List of temperatures from different websites.

        Returns:
            Mean temperature.
        """
        return sum(temperatures) / len(temperatures)

    def accuweather(lat, lon):
        """
        Grab the current temperature from Accuweather at a given lat/lon.

        Args:
            lat:                Latitude of desired location.
            lon:                Longitude of desired location.

        Returns:
              Current temperature in Fahrenheit.
        """
        r = requests.get("http://127.0.0.1:5000/accuweather?latitude={lat}&longitude={lon}".format(lat=lat, lon=lon))
        r = r.json()

        # Pull out weather data.
        weather = r['simpleforecast']['forecastday'][0]

        # Pull out current temperature.
        return float(weather['current']['fahrenheit'])

    def noaa(lat, lon):
        """
        Grab the current temperature from NOAA at a given lat/lon.

        Args:
            lat:                Latitude of desired location.
            lon:                Longitude of desired location.

        Returns:
              Current temperature in Fahrenheit.
        """
        r = requests.get("http://127.0.0.1:5000/noaa?latlon={lat},{lon}".format(lat=lat, lon=lon))
        r = r.json()

        # Pull out today's weather data.
        weather = r['today']

        # Pull out current temperature.
        return float(weather['current']['fahrenheit'])

    def weatherdotcom(lat, lon):
        """
        Grab the current temperature from Weather.com at a given lat/lon.

        Args:
            lat:                Latitude of desired location.
            lon:                Longitude of desired location.

        Returns:
              Current temperature in Fahrenheit.
        """
        r = requests.post('http://127.0.0.1:5000/weatherdotcom', json={"lat": lat, "lon": lon})
        r = r.json()

        # Pull out current temperature in one line. The dictionary keys here are non-intuitive, so having two
        #  lines for the data grab is unneccessary.
        return float(r['query']['results']['channel']['ttl'])

    # Initialize site filters to None. This will prevent a NameError later on when we attempt to iterate through
    #  site filters.
    site_filters = None

    # Verify the user did not supply an unsupported site filter.
    if kwargs:
        site_filters = set(kwargs.values())
        if not site_filters.issubset({'accuweather', 'noaa', 'weather.com'}):
            return HttpResponse('Unsupported site filter supplied. We currently support accuweather, noaa, and weather.com.')

    # Verify the lat and lon are numeric.
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return HttpResponse('Must provide numeric latitude and longitude.')

    # Initialize list that will hold temperatures.
    all_temperatures = []

    # If there are no site filters, grab all three temperatures.
    if not site_filters:
        accuweather = accuweather(lat, lon)
        all_temperatures.append(accuweather)
        noaa = noaa(lat, lon)
        all_temperatures.append(noaa)
        weatherdotcom = weatherdotcom(lat, lon)
        all_temperatures.append(weatherdotcom)

    # If there are site filters, only grab temperatures for the filter sites.
    else:
        if 'accuweather' in site_filters:
            accuweather = accuweather(lat, lon)
            all_temperatures.append(accuweather)

        if 'noaa' in site_filters:
            noaa = noaa(lat, lon)
            all_temperatures.append(noaa)

        if 'weather.com' in site_filters:
            weatherdotcom = weatherdotcom(lat, lon)
            all_temperatures.append(weatherdotcom)

    # Calculate the mean of the temperatures.
    average_temp = mean(all_temperatures)

    # Round to whole number for clean output.
    average_temp = int(average_temp)

    return JsonResponse({'average_fahrenheit_temperature': average_temp})
