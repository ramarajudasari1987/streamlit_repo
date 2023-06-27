# streamlit_app.py
import os
import pathlib
import streamlit as st
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import psycopg2

import pandas as pd



# Initialize connection.
# Uses st.cache_resource to only run once.conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
conn = init_connection()

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


# @st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    # return file
def get_data_filter(title, force):
    cur = conn.cursor()
    cur.execute("SELECT * from gun_info where column_c = %s AND  column_g = %s",(title,force,))
    rows = cur.fetchall()
    # rows = run_query("SELECT * from gun_info where column_c=? and where column_g=?;")
    par_path = pathlib.Path(__file__).parent.resolve().parent
    image_src_list = []

    for row in rows:
        ID = row[0]

        image = row[8]
        photo = os.path.join(par_path, r"static/img{0}.jpg".format(ID))
        photo1 = r"/app/static/img{0}.jpg".format(ID)
        write_file(image, photo)   
        image_src_list.append(photo1)

    df = pd.DataFrame(rows, columns=['column_a', 'column_b', 'column_c', 'column_d', 'column_e', 'column_f',
                    'column_g', 'column_h', 'column_i', 'column_j', 'column_k', 'column_l', 'column_m', 'column_n'])
    df = df.drop('column_i', axis=1)
    df.insert(8, "image_loc", image_src_list, True)
    ob = GridOptionsBuilder.from_dataframe(df)

    image_render = JsCode("""
    class ThumbnailRenderer {
    init(params) {
    this.eGui = document.createElement('img');
    this.eGui.setAttribute('src', params.value);
    this.eGui.setAttribute('width', '100');
    }
    getGui() {
    return this.eGui;
    }
    }
    """)

    ob.configure_column("image_loc" ,"photo", cellRenderer=image_render)
    ob.configure_default_column(wrapText=True, autoHeight=True)
    grid_options=ob.build()
    grid = AgGrid(df, gridOptions=grid_options, theme="streamlit",
                allow_unsafe_jscode=True, width=500)
    st.set_page_config(page_title="test", layout="wide")
def get_data():
    cur = conn.cursor()
    cur.execute("SELECT * from gun_info;")
    rows = cur.fetchall()
    # rows = run_query("SELECT * from gun_info where column_c=? and where column_g=?;")
    par_path = pathlib.Path(__file__).parent.resolve().parent
    image_src_list = []

    for row in rows:
        ID = row[0]

        image = row[8]
        photo = os.path.join(par_path, r"static/img{0}.jpg".format(ID))
        photo1 = r"/app/static/img{0}.jpg".format(ID)
        write_file(image, photo)   
        image_src_list.append(photo1)
    st.set_page_config(page_title="test", layout="wide")
    df = pd.DataFrame(rows, columns=['column_a', 'column_b', 'column_c', 'column_d', 'column_e', 'column_f',
                    'column_g', 'column_h', 'column_i', 'column_j', 'column_k', 'column_l', 'column_m', 'column_n'])
    df = df.drop('column_i', axis=1)
    df.insert(1, "image_loc", image_src_list, True)
    ob = GridOptionsBuilder.from_dataframe(df)

    image_render = JsCode("""
    class ThumbnailRenderer {
    init(params) {
    this.eGui = document.createElement('img');
    this.eGui.setAttribute('src', params.value);
    this.eGui.setAttribute('width', '100');
    }
    getGui() {
    return this.eGui;
    }
    }
    """)

    ob.configure_column("image_loc" ,"photo", cellRenderer=image_render)
    ob.configure_default_column(wrapText=True, autoHeight=True)
    grid_options=ob.build()
    grid = AgGrid(df, gridOptions=grid_options, theme="streamlit",
                allow_unsafe_jscode=True, width=500)
    
get_data()
# title = st.text_input('Enter Value')
# force = st.radio("select force",("16/16","20/20"))
# st.button("GET DATA",on_click=get_data, args=(title,force))
# @st.cache_resource





    


