# https://python-visualization.github.io/folium/quickstart.html
import os
import json

import pandas as pd
import numpy as np
import folium


# Nanjing latitude and longtitude
latitude, longtitude = 32.04, 118.78

# Nanjing geometric json data
with open("nanjing.json", 'r', encoding='utf-8') as f:
    nanjing_geo = json.loads(f.read())

# read covid data
infection_frame = pd.read_csv('data.csv', header=0, dtype={'number':np.int32})
infection_map = dict(zip(infection_frame['district'], infection_frame['number']))

# plot map
nanjing_map = folium.Map(
    location=[latitude, longtitude],
    tiles="cartodbpositron",
    zoom_start=9)

# plot geometric bound
folium.GeoJson(
    data = nanjing_geo,
    name="geojson",
    zoom_on_click=True,
    style_function=lambda feature: {
        'fillColor': '#ffff00',
        'color': 'red',
        'weight': '2',
    }
).add_to(nanjing_map)

# plot COVID data
folium.Choropleth(
    geo_data=nanjing_geo,
    name="choropleth",
    data=infection_frame,
    columns=["district", "number"],
    key_on="feature.properties.name",
    highlight=True,
    fill_color='BuPu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Number of Infected",
).add_to(nanjing_map)
folium.LayerControl().add_to(nanjing_map)

# add markers
for district in nanjing_geo['features']:
    lon, lat = district['properties']['centroid']
    loc = district['properties']['name']
    s = f"{loc} 共{infection_map[loc]}例确诊"
    folium.Marker(
        location=[lat, lon],
        tooltip=s,
        icon=folium.Icon(color='blue')
    ).add_to(nanjing_map)

nanjing_map.save('folium.html')
os.system("start ./folium.html")