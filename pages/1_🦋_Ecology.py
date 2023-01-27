import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_elements import elements, mui, html, dashboard

import folium
from folium import plugins
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
from shapely import Point, LineString, Polygon

import altair as alt

# create exagons
from h3 import h3




st.set_page_config(page_title="Ecology", page_icon="🦋",layout="wide")

                
import requests
import streamlit as st
from base64 import b64encode
from streamlit_elements import elements, dashboard, html

st.set_page_config(layout="wide")

# Some random image URL.
images_url = [
    "https://unsplash.com/photos/1CsaVdwfIew/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjUxNTE3OTQx&force=true&w=1920",
    "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
    "https://unsplash.com/photos/CSs8aiN_LkI/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjUxNTE2ODM1&force=true&w=1920",
    "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
]

# Download these images and get their bytes.
images_bytes = [requests.get(url).content for url in images_url]

# Encode these bytes to base 64.
images_b64 = [b64encode(bytes).decode() for bytes in images_bytes]

# Initialize a layout for our dashboard.
# It's gonna be a 2x2 grid, with each element being of height 3 and width 6 out of 12.
layout = [
    dashboard.Item("image0", 0, 0, 6, 3),
    dashboard.Item("image1", 6, 0, 6, 3),
    dashboard.Item("image2", 0, 3, 6, 3),
    dashboard.Item("image3", 6, 3, 6, 3),
]

with elements("image_grid"):
    with dashboard.Grid(layout):
        # We iterate over our images encoded as base64.
        # enumerate() will return the item's index i from 0 to 3, so I can generate
        # dashboard layout keys from "image0" to "image3".
        for i, b64 in enumerate(images_b64):
            html.img(
                # We pass our base 64 to <img src=...></img> to display our image.
                # See: https://stackoverflow.com/a/8499716
                src=f"data:image/png;base64,{b64}",
                # A simple CSS style to avoid image distortion on resize.
                css={"object-fit": "cover"},
                # We set the key to bind our image to a dashboard item.
                key=f"image{i}",
            )"---"

df_raw = pd.read_csv('pages/bird_migration (1).csv')

# convert in date_time data
df_raw["date_time"] = pd.to_datetime(df_raw["date_time"])
df_1 = df_raw[['date_time','bird_name', 'latitude', 'longitude']]
df_1['month'] = df_1.date_time.dt.month_name()

st.subheader("Calculate the distance covered per month")

#zip the coordinates into a point object and convert to a GeoData Frame
geometry = [Point(xy) for xy in zip(df_1.longitude,df_1.latitude,)]
geo_df = gpd.GeoDataFrame(df_1, geometry=geometry)
geo_df = geo_df.groupby(['bird_name','month'])['geometry'].apply(lambda x:LineString(x.tolist()))
geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry',crs={'init':'epsg:4326'}).reset_index()
geo_df.to_crs(epsg=3310,inplace=True)
geo_df['distance (Km)'] = round(geo_df.length / 1000)

source = pd.DataFrame(geo_df.drop(columns='geometry'))

altair_chart = alt.Chart(source).mark_bar(
).encode(
x=alt.X('bird_name:N',title=''),
y='distance (Km):Q',
color='bird_name:N',
column=alt.Column('month:N',
                  align="all",
                  sort=['August','September','October','November', 'December','January', 'February', 'March','April'])
)

st.altair_chart(altair_chart, use_container_width=False, theme=None)

"---"

st.subheader("Show the routes through the time")

df_Eric = df_raw[df_raw.bird_name=='Eric'].reset_index(drop=True)
df_Eric['date_time'] = df_Eric['date_time'].dt.date
df_Nico = df_raw[df_raw.bird_name=='Nico'].reset_index(drop=True)
df_Nico['date_time'] = df_Nico['date_time'].dt.date
df_Sanne = df_raw[df_raw.bird_name=='Sanne'].reset_index(drop=True)
df_Sanne['date_time'] = df_Sanne['date_time'].dt.date



lat = df_raw.latitude.mean()
long = df_raw.longitude.mean()

m = folium.Map(location=[lat,long],zoom_start=3,tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr='Google_map')


lines = [
{
    "coordinates": [[df_Eric.longitude[i],df_Eric.latitude[i]] for i in range(len(df_Eric))],
    "dates": df_Eric.date_time.astype(str).tolist(),
    "color": "red",
},
{
    "coordinates": [[df_Nico.longitude[i],df_Nico.latitude[i]] for i in range(len(df_Nico))],
    "dates": df_Nico.date_time.astype(str).tolist(),
    "color": "blue",
},
{
    "coordinates": [[df_Sanne.longitude[i],df_Sanne.latitude[i]] for i in range(len(df_Sanne))],
    "dates": df_Sanne.date_time.astype(str).tolist(),
    "color": "purple",
}
]

features = [
{
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": line["coordinates"],
    },
    "properties": {
        "times": line["dates"],
        "style": {
            "color": line["color"],
            "weight": line["weight"] if "weight" in line else 2,
        },
        "popup": "Eric" if line["color"]== "red"  else "Nico" if line["color"]== "blue" else 'Sanne',
        "icon": "marker",
        "iconstyle": {
            "iconUrl":  "https://img.icons8.com/color/48/26e07f/seagull--v2.png" if line["color"]== "red"  else "https://img.icons8.com/fluency/48/000000/seagull.png",
            "iconSize": [50,50],
        }
    },
}
for line in lines
]

plugins.TimestampedGeoJson(
{
    "type": "FeatureCollection",
    "features": features,
},
period="P1D",
add_last_point=True,
date_options='YYYY-MM-DD',
loop_button=True,
loop=False,).add_to(m)

plugins.Fullscreen().add_to(m)

st_folium(m)

"---"

st.subheader("Find the pricese moment and the place where they met (if there are)")



h3_level = 14 # ~6m2 area resolution
 
def lat_lng_to_h3(row):
    return h3.geo_to_h3(row.geometry.y, row.geometry.x, h3_level)
 
#zip the coordinates into a point object and convert to a GeoData Frame
geometry = [Point(xy) for xy in zip(df_1.longitude, df_raw.latitude)]
df_points = gpd.GeoDataFrame(df_1, geometry=geometry,crs="EPSG:4326")
df_points['h3'] = df_points.apply(lat_lng_to_h3, axis=1)
df_points['Date'] = df_points['date_time'].dt.to_period('D')

df_pol = df_points.groupby(['h3','Date','bird_name'],as_index=False).size()
df_pol = df_pol[df_pol.duplicated(subset=['h3','Date'],keep=False)]

# create a dataset with the geometry of the exagons and the number of earthquakes and max magnitudo 
 
def add_geometry(row):
    points = h3.h3_to_geo_boundary(
      row['h3'], True)
    return Polygon(points)


df_pol['geometry'] = df_pol.apply(add_geometry, axis=1)
df_pol = gpd.GeoDataFrame(df_pol, crs='EPSG:4326')

df_point = df_points.merge(df_pol[['h3','Date']],on=['h3','Date'],how='right') \
.drop_duplicates().reset_index(drop=True)

df_point['time'] = df_point['date_time'].dt.time

distance = df_point.to_crs({'init': 'epsg:6933'}).loc[0,'geometry'].distance(df_point.to_crs({'init': 'epsg:6340'}).loc[1,'geometry'])
distance_2 = df_point.to_crs({'init': 'epsg:6933'}).loc[2,'geometry'].distance(df_point.to_crs({'init': 'epsg:6340'}).loc[3,'geometry'])

left, right = st.columns([1,2])
with left:
  f"""
  On 25th April 2014, Nico and Eric where at 20:09 and 21:13 respectively at {round(distance,2)} meters distance each other.
  It is highly probable that they met between 20:00 and 21:30.

  Eric and Sanne were nearby on the same day too ({round(distance_2,2)} meters), but the time gap is too wide that probably 
  they did't cross each other. 
  """

with right:

  df_base = df_point[['bird_name', 'geometry']].loc[:1]

  # create a map
  centroid = df_base.centroid
  m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=15,tiles='OpenStreetMap')


  style_function = lambda x: {'fillColor': '#0000ff' if
                               x['properties']['bird_name']=='Eric' else
                               '#00ff00'}

  folium.GeoJson(data=df_base,
                 style_function=style_function,
                 tooltip=folium.GeoJsonTooltip(['bird_name'],labels=True,),
                ).add_to(m)



  st_folium(m)

"---"

st.subheader("Create a choropleth using the H3 geospatial indexing system to show where the birds spent more time.")

h3_level = 6 #~35Km2
 
def lat_lng_to_h3(row):
    return h3.geo_to_h3(row.geometry.y, row.geometry.x, h3_level)
 
#zip the coordinates into a point object and convert to a GeoData Frame
geometry = [Point(xy) for xy in zip(df_1.longitude, df_raw.latitude)]
geo_df = gpd.GeoDataFrame(df_1, geometry=geometry,crs="EPSG:4326")
geo_df['h3'] = geo_df.apply(lat_lng_to_h3, axis=1)
geo_df['Date'] = geo_df['date_time'].dt.to_period('D')
geo_df.head()

df_hexagon = geo_df.groupby(['bird_name','h3']).agg(number_of_points = ('h3','count')).reset_index()

def add_geometry(row):
    points = h3.h3_to_geo_boundary(
      row['h3'], True)
    return Polygon(points)


df_hexagon['geometry'] = df_hexagon.apply(add_geometry, axis=1)
df_hexagon = gpd.GeoDataFrame(df_hexagon, crs="EPSG:4326")

df_base = df_hexagon


# create a map
centroid = df_base.centroid
m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=4,control_scale=False,tiles=None )

tile_layer = folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
    attr='Google_map',
    control=False,
    opacity=1
)
tile_layer.add_to(m)


for var in df_base['bird_name'].unique():
    df_geo = df_base[df_base['bird_name']==var]
    
    c = folium.Choropleth(
        geo_data=df_geo.to_json(),
        name=var,
        data=df_geo,
        columns=["h3", 'number_of_points'],
        key_on="feature.properties.h3",
        fill_color='Reds',
        fill_opacity=0.6,
        legend_name=var,
        overlay=False,
        highlight=True,
        line_opacity=.8,
    ).add_child(folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr='Google_map')).add_to(m)
    
    
    for key in list(c._children):
        if key.startswith('color_map'):
            del(c._children[key])
   
    c.geojson.add_child(folium.features.GeoJsonTooltip(fields=['number_of_points'],
                                                       aliases=['number_of_points'],
                                                       style=('background-color: white; color: black; font-family:''Courier New; font-size: 12px; padding: 10px;')
                                                      )
                       )
    


# Add a layer control panel to the map.
m.add_child(folium.LayerControl(collapsed=True))

#fullscreen
folium.plugins.Fullscreen().add_to(m)


st_folium(m)


#####

import pydeck as pdk

dict_df = {"df_Eric" : df_raw[df_raw.bird_name=='Eric'].reset_index(drop=True),
           "df_Nico" : df_raw[df_raw.bird_name=='Nico'].reset_index(drop=True),
           "df_Sanne" : df_raw[df_raw.bird_name=='Sanne'].reset_index(drop=True)}

col_1,col_2,col_3 =st.columns(3)
x = [col_1,col_2,col_3]
y = dict_df.keys()
for col, df in zip(x, y):
    with col:
        st.write(df)
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=dict_df[df]["latitude"].mean(),
                longitude=dict_df[df]["longitude"].mean(),
                zoom=3,
                pitch=100,
            ),
            layers=[
                pdk.Layer(
                   'HexagonLayer',
                   data=dict_df[df][["longitude", "latitude"]],
                   get_position=["longitude", "latitude"],
                   radius=2000,
                   elevation_scale=4,
                   elevation_range=[0, 10000],
                   pickable=True,
                   extruded=True,
                )
            ],
        ))


