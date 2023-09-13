import streamlit as st
import pandas as pd
import math
from itertools import compress

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     

st.title("Catálogo Vídeos")

st.subheader('Escoge los vídeos que quieras usar.')

#We call our videos DB 

df = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv')
df = df[(df['Components']==1)& (df['Activo']=='Si')]


idioma = st.selectbox('Elige el idioma de los vídeos', ('Español','Inglés','Portugués'), index=0)

#[canciones, cuquines,otros] =st.tabs(['Canciones','Cuquines', 'Otros'])
[canciones, cuquines] =st.tabs(['Canciones','Cuquines'])

if idioma!='Ninguno':
    selected_videos =pd.DataFrame(columns =list(df.columns))
    with canciones:
        canciones_df = df[(df['Language']==idioma) & (df['Category']=='Music')]
        num_columns1 = 4
        num_rows1 = math.ceil(len(canciones_df) / num_columns1)
        for row1 in range(num_rows1):
            row_items1 = canciones_df['Name'][row1*num_columns1: (row1+1)*num_columns1]
            columns1 = st.columns(num_columns1)
            for col_idx1, item1 in enumerate(row_items1):
                checkbox_state1 = columns1[col_idx1].checkbox(item1,key=str(col_idx1) + item1+str(row_items1))
                if checkbox_state1:
                   # selected_videos = selected_videos.append(canciones_df[canciones_df['Name'] == item1])
                   selected_videos = pd.concat([selected_videos, canciones_df[canciones_df['Name'] == item1]], ignore_index=True)

    with cuquines:                 
        cuquines_df = df[(df['Language']==idioma) & (df['Category']=='Education')]
        num_columns2 = 4
        num_rows2 = math.ceil(len(cuquines_df) / num_columns2)
        for row2 in range(num_rows2):
            row_items2 = cuquines_df['Name'][row2*num_columns2: (row2+1)*num_columns2]
            columns2 = st.columns(num_columns2)

            for col_idx2, item2 in enumerate(row_items2):
                checkbox_state = columns2[col_idx2].checkbox(item2,key=str(col_idx2) + item2+str(row_items2))
                if checkbox_state:
                    selected_videos = pd.concat([selected_videos, cuquines_df[cuquines_df['Name'] == item2]], ignore_index=True)

    # with otros:
    #     otros_df =df[((df['Language']==idioma) & (df['Category'] !='Education') & (df['Category']!='Music')) | (df['Name']=='Intro')]
    #     num_columns3 = 4
    #     num_rows3 = math.ceil(len(otros_df) / num_columns3)
    #     for row3 in range(num_rows3):
    #         row_items3 = otros_df['Name'][row3*num_columns3: (row3+1)*num_columns3]
    #         columns3 = st.columns(num_columns3)

    #         for col_idx3, item3 in enumerate(row_items3):
    #             checkbox_state = columns3[col_idx3].checkbox(item3,key=str(col_idx3) + item3+str(row_items3))
    #             if checkbox_state:
    #                 selected_videos = pd.concat([selected_videos, otros_df[otros_df['Name'] == item3]], ignore_index=True)
        
    st.dataframe(selected_videos[['Path','Filename','Name','Language','Category','Tag_IP','Tag_pieza']], use_container_width=True)
    
else:  st.info('Por favor, elige un lenguaje:')

if st.sidebar.button('Guardar selección de vídeos'):    
    st.session_state['selected_videos'] = selected_videos
    st.session_state['idioma'] = idioma
    