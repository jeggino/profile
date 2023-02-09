import streamlit as st
from streamlit_option_menu import option_menu

import folium
from streamlit_folium import st_folium

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

import altair as alt
from vega_datasets import data

st.set_page_config(
    page_title="Profile",
    page_icon="🧊",
    layout="wide",
)



df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

# ---PLOT 1---


source = data.seattle_weather()

scale = alt.Scale(domain=['sun', 'fog', 'drizzle', 'rain', 'snow'],
                  range=['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4', '#9467bd'])
color = alt.Color('weather:N', scale=scale)

# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=['x'])
click = alt.selection_multi(encodings=['color'])

# Top panel is scatter plot of temperature vs time
points = alt.Chart().mark_point().encode(
    alt.X('monthdate(date):T', title='Date'),
    alt.Y('temp_max:Q',
        title='Maximum Daily Temperature (C)',
        scale=alt.Scale(domain=[-5, 40])
    ),
    color=alt.condition(brush, color, alt.value('lightgray')),
    size=alt.Size('precipitation:Q', scale=alt.Scale(range=[5, 200]))
).add_selection(
    brush
).transform_filter(
    click
)

# Bottom panel is a bar chart of weather type
bars = alt.Chart().mark_bar().encode(
    x='count()',
    y='weather:N',
    color=alt.condition(click, color, alt.value('lightgray')),
).transform_filter(
    brush
).add_selection(
    click
)

plot_1 = alt.vconcat(
    points,
    bars,
    data=source,
    title="Seattle Weather: 2012-2015"
)

# ---PLOT 2---
source = data.disasters.url

plot_2 = alt.Chart(source).mark_circle(
    opacity=0.8,
    stroke='black',
    strokeWidth=1
).encode(
    alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
    alt.Y('Entity:N'),
    alt.Size('Deaths:Q',
        scale=alt.Scale(range=[0, 4000]),
        legend=alt.Legend(title='Annual Global Deaths')
    ),
    alt.Color('Entity:N', legend=None)
).transform_filter(
    alt.datum.Entity != 'All natural disasters'
)


# ---PLOT 3---
source = data.movies.url

pts = alt.selection(type="single", encodings=['x'])

rect = alt.Chart(data.movies.url).mark_rect().encode(
    alt.X('IMDB_Rating:Q', bin=True),
    alt.Y('Rotten_Tomatoes_Rating:Q', bin=True),
    alt.Color('count()',
        scale=alt.Scale(scheme='greenblue'),
        legend=alt.Legend(title='Total Records')
    )
)

circ = rect.mark_point().encode(
    alt.ColorValue('grey'),
    alt.Size('count()',
        legend=alt.Legend(title='Records in Selection')
    )
).transform_filter(
    pts
)

bar = alt.Chart(source).mark_bar().encode(
    x='Major_Genre:N',
    y='count()',
    color=alt.condition(pts, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
).add_selection(pts)

plot_3 = alt.vconcat(
    rect + circ,
    bar
).resolve_legend(
    color="independent",
    size="independent"
)

# ---MAP---
counties = alt.topo_feature(data.us_10m.url, 'counties')
source = data.unemployment.url

map_1 = alt.Chart(counties).mark_geoshape().encode(
    color='rate:Q'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(source, 'id', ['rate'])
).project(
    type='albersUsa'
)

# ---DASHBOARD---
col1, col2 = st.columns([1, 1],gap="medium")
col3, col4, col5 = st.columns([2, 1, 1],gap="medium")


with col1:
    st.altair_chart(plot_1, use_container_width=False, theme="streamlit")
with col2:
    st.altair_chart(plot_2, use_container_width=False, theme="streamlit")
with col3:
    st.altair_chart(plot_3, use_container_width=False, theme="streamlit")
with col4:
    st.altair_chart(map_1, use_container_width=False, theme="streamlit") 
with col5:
    st.dataframe(df,use_container_width=False)


