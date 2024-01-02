import streamlit as st
from PIL import Image

import pandas as pd
import time
import pymysql

import serial


st.set_page_config(
    page_title="Smart Socket",
    layout="wide",
)

if 'on_state3' not in st.session_state:
    st.session_state.on_state3 = False
    
if 'on_state2' not in st.session_state:
    st.session_state.on_state2 = False 
        
if 'on_state1' not in st.session_state:
    st.session_state.on_state1 = False 


def generate_data(num):
    Title = time.strftime("sss%Y%m%d")
    db = pymysql.connect(host="localhost", user="root", password="password", charset="utf8")
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute('USE sensor;')

    select_query = f'SELECT * FROM {Title}'
    cursor.execute(select_query)

    df_org = cursor.fetchall()
    df_org = pd.DataFrame(df_org)
    df = pd.DataFrame(df_org, columns=[f'pw{num}', f'total{num}'])
    df['time'] = pd.DataFrame(df_org, columns=['time'])

    return df


def main_page():        
    st.title("Smart Socket")


def page1():
    
    # st.sidebar.markdown("# Socket 1")

    tab1, tab2, tab3 = st.tabs(["socket1", "socket2", "socket3"])

    with tab1:
        st.title("Socket 1")

        st.session_state.on_state1 = st.toggle("Switch1", st.session_state.on_state1)

        if st.session_state.on_state1:
            image = Image.open('img/on.png')
            # py_serial.write(b'1')
        else:
            image = Image.open('img/off.png')
            # py_serial.write(b'2')

        st.image(image)

    with tab2:
        st.title("Socket 2")

        st.session_state.on_state2 = st.toggle("Switch1", st.session_state.on_state1)

        if st.session_state.on_state2:
            image = Image.open('img/on.png')
            # py_serial.write(b'1')
        else:
            image = Image.open('img/off.png')
            # py_serial.write(b'2')

        st.image(image)

    with tab3:
        st.title("Socket 3")

        st.session_state.on_state3 = st.toggle("Switch1", st.session_state.on_state)

        if st.session_state.on_state1:
            image = Image.open('img/on.png')
            # py_serial.write(b'1')
        else:
            image = Image.open('img/off.png')
            # py_serial.write(b'2')

        st.image(image)

        

    


def page2():
    
    st.sidebar.markdown("# Socket 2")

    tab1, tab2 = st.tabs(["power", "graph"])

    with tab1:
        st.title("Socket2")

        st.session_state.on_state2 = st.toggle("Switch2", st.session_state.on_state2)

        if st.session_state.on_state2:
            image = Image.open('img/on.png')
            # py_serial.write(b'3')
        else:
            image = Image.open('img/off.png')
            # py_serial.write(b'4')

        st.image(image)

        

    with tab2:
        col1, col2 = st.columns(2)
        
        data = generate_data(2)
        data2 = pd.DataFrame(data, columns=['pw2', 'time'])
        chart = st.line_chart(data2.set_index("time"))
        ph1 = st.empty()
        ph2 = st.empty()
        
        while True:
            global last_value
            time.sleep(1)
            new_data = generate_data(2)
            new_data2 = pd.DataFrame(new_data, columns=['pw2', 'time'])
            
            data = pd.concat([data, new_data])
            data2 = pd.concat([data2, new_data2])
            chart.line_chart(data2.set_index("time").tail(60))
            last_value = data.iloc[-1, 0]
            last_value_total = data.iloc[-1, 1]
            ph1.metric(
                label="Current Usage",
                value=f"{last_value} KWh"
            )

            ph2.metric(
                label="Monthly Usage",
                value=f"{last_value_total} KWh",
            )



def page3():
    st.sidebar.markdown("# Socket 3")

    tab1, tab2 = st.tabs(["power", "graph"])

    with tab1:
        st.title("Socket3")

        st.session_state.on_state3 = st.toggle("Switch3", st.session_state.on_state3)

        if st.session_state.on_state3:
            image = Image.open('img/on.png')
            # py_serial.write(b'5')

        else:
            image = Image.open('img/off.png')
            # py_serial.write(b'6')


        st.image(image)

        

    with tab2:
        col1, col2 = st.columns(2)
        
        data = generate_data(3)
        
        data2 = pd.DataFrame(data, columns=['pw3', 'time'])
        chart = st.line_chart(data2.set_index("time"))
        ph1 = st.empty()
        ph2 = st.empty()
        
        while True:
            global last_value
            time.sleep(1)
            new_data = generate_data(3)
            new_data2 = pd.DataFrame(new_data, columns=['pw3', 'time'])
            
            data = pd.concat([data, new_data])
            last_value = data.iloc[-1, 0]
            last_value_total = data.iloc[-1, 1]
            ph1.metric(
                label="Current Usage",
                value=f"{last_value} KWh"
            )

            ph2.metric(
                label="Monthly Usage",
                value=f"{last_value_total} KWh",
            )



page_names_to_funcs = {
    "Main page": main_page,
    "Socket Control": page1,
    "Power Usage": page2,
    "socket3": page3
    
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
