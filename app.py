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






from st_aggrid import JsCode, AgGrid, GridOptionsBuilder





headers = ["symboling", "normalized_losses", "make", "fuel_type", "aspiration",
           "num_doors", "body_style", "drive_wheels", "engine_location",
           "wheel_base", "length", "width", "height", "curb_weight",
           "engine_type", "num_cylinders", "engine_size", "fuel_system",
           "bore", "stroke", "compression_ratio", "horsepower", "peak_rpm",
           "city_mpg", "highway_mpg", "price"]

df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data",
                 names=headers, 
                 na_values="?" 
                )
df = df[['wheel_base', 'length', 'width', 'height','horsepower', 'peak_rpm',  'price', 'fuel_type','num_doors','engine_type']]

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gridOptions = gb.build()
dta = AgGrid(df, gridOptions=gridOptions,height=350, allow_unsafe_jscode=True, enable_enterprise_modules=True)

st.write(dta['selected_rows'])
