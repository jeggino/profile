import streamlit as st
from streamlit_option_menu import option_menu
from st_on_hover_tabs import on_hover_tabs

import folium
from folium import plugins
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
from shapely import Point, LineString

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

from st_aggrid import AgGrid




st.set_page_config(page_title="Ecology", page_icon="🦋")



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


st.subheader("Show the routes through the time")

df_Eric = df_raw[df_raw.bird_name=='Eric'].reset_index(drop=True)
df_Eric['date_time'] = df_Eric['date_time'].dt.date
df_Nico = df_raw[df_raw.bird_name=='Nico'].reset_index(drop=True)
df_Nico['date_time'] = df_Nico['date_time'].dt.date
df_Sanne = df_raw[df_raw.bird_name=='Sanne'].reset_index(drop=True)
df_Sanne['date_time'] = df_Sanne['date_time'].dt.date

import folium
from folium import plugins
from branca.element import Figure



# create the Heatmap
fig=Figure(width=850,height=550)

lat = df_raw.latitude.mean()
long = df_raw.longitude.mean()

m = folium.Map(location=[lat,long],zoom_start=3,tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr='Google_map')

fig.add_child(m)


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


