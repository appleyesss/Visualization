# https://plotly.com/python/
import json

import pandas as pd
import plotly.express as px


# Nanjing geometric json data
with open("nanjing.json", 'r', encoding='utf-8') as f:
    nanjing_geo = json.loads(f.read())

# read covid data
infection_frame = pd.read_csv('data.csv', header=0)
infection_map = dict(zip(infection_frame['district'], infection_frame['number']))

fig = px.choropleth_mapbox(infection_frame,
                           geojson=nanjing_geo,
                           locations='district',
                           featureidkey="properties.name",
                           color='number',
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=7,
                           center={
                               "lat": 32.04,
                               "lon": 118.78
                           },
                           opacity=0.5,
                           labels={'number': 'infection'})
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()