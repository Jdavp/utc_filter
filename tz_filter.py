#!/usr/bin/python3

import requests
import json
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim, GeoNames
from python_countries import CountriesApi


def getcountry(city: str) -> str:
    #get country from city
    num = Nominatim(user_agent='tz_filter')
    place, cord = (lat, lng) = num.geocode(city)
    country = place.split(',')[2]
    return country.strip()

def gettimezone(country: str) -> list:
    #get time zone from country

    if type(country) is list and any("United States" in s for s in country):
        country = [c.replace("United States", "USA") for c in country]
    client = CountriesApi()
    try: 
        if type(country) is list:
            country = client.full_name(country[0])
        else:
            country = client.full_name(country)
        timezone = country[0].get('timezones')
    except:
        timezone = []
    return timezone

def getuserinfo(user_public_id: str) -> dict:
    # get user basic info (picture,username, timezone)
    
    response = requests.get("https://torre.bio/api/bios/{}"
                            .format(user_public_id))

    userpicture = response.json()['person'].get('picture')

    username = response.json()['person'].get('name')

    timezone = response.json()['person']['location'].get('timezone')

    city = timezone.split('/')[1]
    country = getcountry(city)
    utc = gettimezone(country)

    return {"name": username,
            "photo": userpicture,
            "timezone": utc
            }

def opportunitys(utc):
    # get offer in the same time zone

    response = requests.post("https://search.torre.co/opportunities/_search/?offset=0&size=100").json()
    df = pd.json_normalize(response["results"])
    columns = df[["id", 'objective', "locations", "remote"]]
    columns['aretherelocations'] =  columns["locations"].apply(lambda x: 1 if len(x) > 0 else 0)
    offers_remote_location = columns[(columns['remote'] & columns['aretherelocations'] == 1)]
    offers_remote_location['timezone'] = offers_remote_location['locations'].apply(lambda x: gettimezone(x))
    offers_remote_location['same_utc'] = offers_remote_location['timezone'].apply(lambda x: str(utc) in str(x)) 
    df_same_utc = offers_remote_location[offers_remote_location['same_utc'] == True]
    # styles changes to table
    final_df = df_same_utc[["id", 'objective', 'locations']]
    final_df.rename(columns={'id':'Offer Link', 'objective':'Position', 'locations':'Locations'}, inplace=True)
    final_df['Offer Link'] = 'https://torre.co/en/jobs/' + final_df['Offer Link'].astype(str)
    
    return(final_df)