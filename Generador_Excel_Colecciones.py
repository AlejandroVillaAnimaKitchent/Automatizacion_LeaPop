# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 10:28:12 2023

@author: alejandro.villa
"""

import streamlit as st
import pandas as pd
import numpy as np 
import math

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     

st.title("Generador de excel para App colecciones")

st.subheader('Aquí se podrá generar el archivo excel para ingresar a la App creadora de colecciones.')

#We Establish the data needed

collect_df =pd.read_csv(r"\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv")    
collect_df =collect_df[collect_df['Components']==1]

categories = ['Ninguna','Canciones','Cuquines','Promos','Miscelaneas']
languages ={'Ninguno':'Ninguno','Español':'ES','Portugués':'PT','Inglés':'EN'}

columnas = st.columns(2)
#video_type = col3.selectbox('Seleccione el tipo de video',)
idioma = columnas[0].selectbox('Seleccione un idioma',languages.keys())
num_collect = columnas[1].number_input('Establezca la cantidad de colecciones que desea',step=1, value=0, format="%d")
df = collect_df[collect_df['Language']==idioma]
sufijos = ['ra', 'da', 'ra', 'ta', 'ta', 'ta', 'ma', 'va', 'na', 'ma', 'va', 'ma', 'va',
                    'na', 'ma', 'va', 'ma', 'va', 'na', 'va']
videos_selected =pd.DataFrame()
def videos_tabs():
    [canciones, cuquines,otros] =st.tabs(['Canciones','Cuquines','Otros'])
    if idioma!='Ninguno':
        videos_selected =pd.DataFrame(columns =list(df.columns))
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
                       videos_selected =videos_selected.append(canciones_df[canciones_df['Name'] == item1])
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
                        videos_selected = videos_selected.append(cuquines_df[cuquines_df['Name'] == item2])
        with  otros:
            otros_df =df[((df['Language']==idioma) & (df['Category'] !='Education') & (df['Category']!='Music')) | (df['Name']=='Intro')]
            num_columns3 = 4
            num_rows3 = math.ceil(len(otros_df) / num_columns3)
            for row3 in range(num_rows3):
                row_items3 = otros_df['Name'][row3*num_columns3: (row3+1)*num_columns3]
                columns3 = st.columns(num_columns3)

                for col_idx3, item3 in enumerate(row_items3):
                    checkbox_state = columns3[col_idx3].checkbox(item3,key=str(col_idx3) + item3+str(row_items3))
                    if checkbox_state:
                        videos_selected =videos_selected.append(otros_df[otros_df['Name'] == item3])
    
if num_collect>0:
    lalist=[]
    tab_labels =[f'{str(i + 1) + sufijos[i]} Colección'  for i in range(num_collect)]
    tabs2=st.tabs(tab_labels)
    for i in range(num_collect):
        with tabs2[i]:  
            titulo =st.text_input('Ingrese el título de su colección y presione ENTER',key=tabs2[i])
            videos_tabs()
            if titulo:
                la_mini_list =[titulo] + videos_selected['Filename'].tolist()
                lalist.append(la_mini_list)
            else: 
                st.error('Presione Enter para ingresar el título')
    df_final = pd.DataFrame()
    df_final =df_final.transpose()
    st.dataframe(df_final)
    creador =st.button('Crear Excel colecciones')
    nombre_archivo =st.text_input('Escriba el numbre del archivo Excel a crear')
    if creador:
        df_final.to_excel(f'\\\\PEGASO\\Material_Definitivo\\telerin\\COLECCIONES\\Col_{}.xlsx',index=False,header=False)
       
else: st.success('Elija el número de colecciones')


