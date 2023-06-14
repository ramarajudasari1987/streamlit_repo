import streamlit as st
import pandas as pd
import numpy as np
st.title('Uber pickups in NYC')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


def load_data():
    data = pd.read_excel(
        r"SampleData.xlsx", sheet_name=None)

    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Loading data Done..")

st.subheader('Raw data')
st.write(data)
