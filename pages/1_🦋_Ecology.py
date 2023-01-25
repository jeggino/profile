import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_player import st_player

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt





st.set_page_config(page_title="Ecology", page_icon="🦋")


df_raw = pd.read_csv('pages/bird_migration (1).csv')

# some altitude were negative probably a typo 
df_raw.altitude = df_raw.altitude.apply(lambda x: x * -1 if x<0 else x)

# convert in date_time data
df_raw["date_time"] = pd.to_datetime(df_raw["date_time"])
df_1 = df_raw[['date_time','bird_name', 'latitude', 'longitude','altitude']]
df_1['month'] = df_1.date_time.dt.month_name()

st.subheader("Calculate the distance covered per month")

#zip the coordinates into a point object and convert to a GeoData Frame
geometry = [Point(xy) for xy in zip(df_1.longitude,df_1.latitude,)]
geo_df = gpd.GeoDataFrame(df_1, geometry=geometry)

geo_df = geo_df.groupby(['bird_name','month'])['geometry'].apply(lambda x:LineString(x.tolist()))
geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry',crs={'init':'epsg:3310'}).reset_index()
geo_df['distance (Km)'] = round(geo_df.length / 1000)
st.error("ERROR!!!!!!!!!!!!!!")

source = pd.DataFrame(geo_df.drop(columns='geometry'))
st.dataframe(source)

altair_chart = alt.Chart(source).mark_bar(
).encode(
    x=alt.X('bird_name:N',title=''),
    y='distance (Km):Q',
    color='bird_name:N',
    column=alt.Column('month:N',
                      align="all",
                      sort=['August','September','October','November', 'December','January', 'February', 'March','April'])
)

st.altair_chart(altair_chart, use_container_width=True, theme=None)
