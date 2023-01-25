import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_player import st_player

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
import geopandas as gpd
from shapely import Point, LineString

import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt






st.set_page_config(page_title="Ecology", page_icon="🦋")


df_raw = pd.read_csv('pages/bird_migration (1).csv')

# convert in date_time data
df_raw["date_time"] = pd.to_datetime(df_raw["date_time"])
df_1 = df_raw[['date_time','bird_name', 'latitude', 'longitude']]
df_1['month'] = df_1.date_time.dt.month_name()
st.dataframe(df_1)

st.subheader("Calculate the distance covered per month")

#zip the coordinates into a point object and convert to a GeoData Frame
geometry = [Point(xy) for xy in zip(df_1.longitude,df_1.latitude,)]
geo_df = gpd.GeoDataFrame(df_1, geometry=geometry)
geo_df = geo_df.groupby(['bird_name','month'])['geometry'].apply(lambda x:LineString(x.tolist()))
geo_df = gpd.GeoDataFrame(geo_df, geometry='geometry',crs={'init':'epsg:4326'}).reset_index()
geo_df.to_crs(epsg=3310,inplace=True)
geo_df['distance (Km)'] = round(geo_df.length / 1000)
st.error("ERROR!!!!!!!!!!!!!!")

source = pd.DataFrame(geo_df)
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

st.altair_chart(altair_chart, use_container_width=False, theme=None)
