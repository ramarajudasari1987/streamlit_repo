import streamlit as st
import openpyxl
import psycopg2
from openpyxl_image_loader import SheetImageLoader
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from io import BytesIO
import os
import pathlib
import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Initialize connection.
# Uses st.cache_resource to only run once.
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def create_connection():
    # Connect to the database
    # using the psycopg2 adapter.
    # Pass your database name ,# username , password ,
    # hostname and port number
    conn = psycopg2.connect(dbname='streamlit',
                            user='postgres',
                            password='admin123',
                            host='localhost',
                            port='5432')
    # Get the cursor object from the connection object
    curr = conn.cursor()
    return conn, curr


def upload():
    
    
    st.set_page_config(page_title="test", layout="wide")
    xldoc = openpyxl.load_workbook(st.session_state['uploaded_file'])
    # print('file_name_test', uploaded_file)

    sh = xldoc["gun"]
    image_loader = SheetImageLoader(sh)

    # get the image (put the cell you need instead of 'A1')

    # iterate through excel and display data
    par_path = pathlib.Path(__file__).parent.resolve().parent
    image_src_list = []
    data_set = []

    df = pd.DataFrame(columns=['column_a', 'column_b', 'column_c', 'column_d', 'column_e', 'column_f',
                    'column_g', 'column_h', 'column_i', 'column_j', 'column_k', 'column_l', 'column_m', 'column_n'])
    i: int = 1
    try:
        for row in sh:
            if i == 1:
                i += 1
                continue

            image: JpegImageFile = image_loader.get('I'+str(i))
            # image.tobytes()
            # buf = BytesIO()
            # image.save(buf, format='JPEG')
            
            photo = os.path.join(par_path, r"static/img{0}.jpg".format(row[0].value))
            image.save(photo)
            photo1 = r"/app/static/img{0}.jpg".format(row[0].value)
            # write_file(BytesIO(bytes(image), photo)   )
            image_src_list.append(photo1)
            
            data_set.append({'column_a':row[0].value,'column_b': row[1].value, 'column_c':row[2].value, 'column_d':row[3].value, 'column_e':row[4].value, 'column_f':row[5].value,'column_g': row[6].value, 'column_h':row[7].value,'column_j': row[9].value,'column_k': row[10].value, 'column_l':row[11].value, 'column_m':row[12].value, 'column_n':row[13].value})
            i += 1
        df = pd.DataFrame(data_set,columns=['column_a', 'column_b', 'column_c', 'column_d', 'column_e', 'column_f',
                    'column_g', 'column_h',  'column_j', 'column_k', 'column_l', 'column_m', 'column_n'])
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
                

                
        st.success('File uploaded successfully...', icon="✅")

    except Exception as e:
        print(e)

        st.info("Something went wrong. Please verify...")
   


with st.form("upload_form", clear_on_submit=False):
    print('in form')
    uploaded_file = st.file_uploader("Choose a file",key="uploaded_file")
    st.form_submit_button(label="Submit", help=None,
                          on_click=upload)