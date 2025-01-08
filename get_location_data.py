from geopy.geocoders import Nominatim
import json
from time import sleep
countries = {
    'North America': [
        "Washington DC United States",
        "Ottawa Canada",
        "Mexico City Mexico",
        "Guatemala City Guatemala",
        "San Salvador El Salvador",
        "Tegucigalpa Honduras",
        "Managua Nicaragua",
        "San Jose Costa Rica",
        "Panama City Panama"
    ],
    'Caribbean': [
        "Havana Cuba",
        "Santo Domingo Dominican Republic",
        "Port-au-Prince Haiti",
        "Kingston Jamaica",
        "Nassau Bahamas",
        "Port of Spain Trinidad and Tobago",
        "Bridgetown Barbados",
        "Saint John's Antigua and Barbuda",
        "Castries Saint Lucia",
        "Kingstown Saint Vincent and the Grenadines",
        "Roseau Dominica",
        "St. George's Grenada",
        "Basseterre Saint Kitts and Nevis",
    ],
    'South America': [
        "Brasilia Brazil",
        "Buenos Aires Argentina",
        "Lima Peru",
        "Bogota Colombia",
        "Santiago Chile",
        "Caracas Venezuela",
        "Quito Ecuador",
        "La Paz Bolivia",
        "Asuncion Paraguay",
        "Montevideo Uruguay",
        "Georgetown Guyana",
        "Paramaribo Suriname",
    ],
    'Central America': [
        "Belmopan Belize",
        "Guatemala City Guatemala",
        "San Salvador El Salvador",
        "Tegucigalpa Honduras",
        "Managua Nicaragua",
        "San Jose Costa Rica",
        "Panama City Panama",
    ]
}

geocoder = Nominatim(user_agent="makalah_matdis")


def fetch_coordinates(country):
    location = geocoder.geocode(country)
    return (location.latitude, location.longitude) if location else (None, None)


locations = {}

for region, country_list in countries.items():
    locations[region] = {}
    for country in country_list:
        latitude, longitude = fetch_coordinates(country)
        locations[region][country] = {'latitude': latitude, 'longitude': longitude}
        sleep(0.2)


with open('locations.json', 'w') as json_file:
    json.dump(locations, json_file,indent=4)