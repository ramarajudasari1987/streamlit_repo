import streamlit as st
import openpyxl
import psycopg2
from openpyxl_image_loader import SheetImageLoader
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from io import BytesIO
# Initialize connection.
# Uses st.cache_resource to only run once.


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

def upload_data():
    conn, cursor = create_connection()
    try:
        image = st.session_state['gun_image'].read()
        # image = Image.open(st.session_state['gun_image'])        
        # buf = BytesIO()
        # image.save(buf, format='JPEG')
        # drawing = open(st.session_state['gun_image'], 'rb').read()       
        
        
        cursor.execute("INSERT INTO gun_info\
                (column_a,column_b,column_c,column_g,column_k,column_i) " +
                            "VALUES(%s,%s,%s,%s,%s,%s)",
                            (st.session_state['gun_id'], st.session_state['plier_type'], st.session_state['force'], st.session_state['cap'], st.session_state['gun_fifty'],psycopg2.Binary(image),))
                # Commit the changes to the database

        conn.commit()
        print('gun_id',st.session_state['gun_id'])
        st.info("Successfully Inserted....")
    except Exception as e:
        print(e)
        st.info("Something went wrong. Please verify...")
    finally:
        conn.close()
        
def upload():
    
    conn, cursor = create_connection()

    xldoc = openpyxl.load_workbook(st.session_state['uploaded_file'])
    # print('file_name_test', uploaded_file)

    sh = xldoc["gun"]
    image_loader = SheetImageLoader(sh)

    # get the image (put the cell you need instead of 'A1')

    # iterate through excel and display data

    i: int = 1
    try:
        for row in sh:
            if i == 1:
                i += 1
                continue

            image: JpegImageFile = image_loader.get('I'+str(i))

            buf = BytesIO()
            image.save(buf, format='JPEG')

            cursor.execute("INSERT INTO gun_info\
            (column_a,column_b,column_c,column_d,column_e,column_f,column_g,column_h,column_i,column_j,column_k,column_l,column_m,column_n) " +
                           "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value, row[7].value,  psycopg2.Binary(buf.getvalue()), row[9].value, row[10].value, row[11].value, row[12].value, row[13].value))
            # Commit the changes to the database

            conn.commit()

            i += 1
        st.success('File uploaded successfully...', icon="✅")

    except Exception as e:
        print(e)

        st.info("Something went wrong. Please verify...")
    finally:
        conn.close()
force = st.radio("Upload",("File","Form"))
if force  == 'File':

    
    with st.form("upload_file", clear_on_submit=False): 
        uploaded_file = st.file_uploader("Choose a file",key='uploaded_file')       
        st.form_submit_button(label="Submit", help=None,
                            on_click=upload)
else:
    form = st.form("upload_form",clear_on_submit=False)
    print('in form')        
    gun_id = form.text_input('Enter Gun Id:',key="gun_id")
    plier_type = form.radio("Plier",("C","X"),key="plier_type")
    force = form.text_input('Enter Force Value:',key="force")
    cap = form.text_input("Enter Cap Value:",key="cap")
    gun_fifty = form.text_input("Enter Gun Fifty Id:",key="gun_fifty")
    gun_image = form.file_uploader("Upload Gun Image",key="gun_image")
    form.form_submit_button(label="Submit", help=None,
                        on_click=upload_data)
                        