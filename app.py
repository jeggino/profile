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


import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import pandas as pd

df = pd.DataFrame(
    {
        "City": ["San Francisco", "San Jose", "Palo Alto"],
        "Latitude": [37.77, 37.33, 37.44],
        "Longitude": [-122.43, -121.89, -122.14],
    }
)

st.dataframe(df.head())

st.write("This is a kepler.gl map with data input in streamlit")

map_1 = KeplerGl(height=400)
map_1.add_data(
    data=df, name="cities"
)  # Alternative: KeplerGl(height=400, data={"name": df})

keplergl_static(map_1, center_map=True)




# from st_aggrid import JsCode, AgGrid, GridOptionsBuilder






# df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')

# gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_selection(selection_mode="multiple", use_checkbox=True)
# gridOptions = gb.build()
# dta = AgGrid(df, gridOptions=gridOptions,height=350, allow_unsafe_jscode=True, enable_enterprise_modules=True)

# st.write(dta['selected_rows'])
