from haversine import haversine, Unit
import json
import plotly.graph_objects as go
from typing import List, Tuple

class Country:
    __slots__ = ['name', 'latitude', 'longitude']  # Memory optimization
    
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    @property
    def coordinate(self) -> Tuple[float, float]:
        return (self.latitude, self.longitude)

class Countries:
    def __init__(self):
        self.countries: List[Country] = []

    def get_distance(self, name1: str, name2: str) -> float:
        country1 = next((c for c in self.countries if c.name == name1), None)
        country2 = next((c for c in self.countries if c.name == name2), None)
        if country1 and country2:
            return haversine(country1.coordinate, country2.coordinate, unit=Unit.KILOMETERS)
        return float('inf')

    def get_adj_matrix(self) -> List[List[float]]:
        n = len(self.countries)
        # Initialize matrix with comprehension
        return [[self.get_distance(self.countries[i].name, self.countries[j].name) 
                for j in range(n)] for i in range(n)]

    def parse_json_countries(self, n: int) -> None:
        with open('locations.json') as json_file:
            data = json.load(json_file)
            count = 0
            # Optimize parsing using itertools
            for region_data in data.values():
                for country, coord in region_data.items():
                    if count >= n:
                        return
                    self.countries.append(Country(
                        country, 
                        coord['latitude'], 
                        coord['longitude']
                    ))
                    count += 1

    def parse_json_by_region(self, region: str) -> None:
        with open('locations.json') as json_file:
            data = json.load(json_file)
            if region in data:
                self.countries.extend(
                    Country(country, coord['latitude'], coord['longitude'])
                    for country, coord in data[region].items()
                )
    def print_countries_path(self, path):
        for i in path:
            print(self.countries[i].name, end=" -> ")

    def plot_lines(self, path: List[int]) -> None:
        # Optimize data preparation using list comprehension
        coordinates = [(self.countries[i].latitude, self.countries[i].longitude) 
                      for i in path]
        lat, lon = zip(*coordinates)

        fig = go.Figure(go.Scattermapbox(
            mode="markers+lines",
            lon=lon,
            lat=lat,
            marker={'size': 5, 'color': 'blue'},
            line={'color': '#FF4136', 'width': 1.5}  # vibrant red color
        ))

        fig.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
            mapbox={
            'style': "carto-positron",  # using light theme for better visualization
            'center': {'lon': 0, 'lat': 20},  # adjusted center for better world view
            'zoom': 4  # slightly adjusted zoom
            }
        )

        fig.show()