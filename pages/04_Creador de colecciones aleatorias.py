# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     

st.title("Creador  de colecciones Aleatorias")

st.subheader('Aquí se podrá crear los archivos excel para usar en la aplicación App Colecciones Lea & Pop')

#We Establish the data needed
Promos_Intro_df = pd.read_csv(r"\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Promos_Intro_LeaPop.csv")

# collect_df =pd.read_csv(r"\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv")    


if 'selected_videos' in st.session_state:
    df_videos = st.session_state['selected_videos']
    selected = list(st.session_state['selected_videos'].Name.unique())
    df = df_videos
    # st.text(selected[0])
else:
    st.info('No hay vídeos seleccionados')   

if 'idioma' in st.session_state:
    idioma = st.session_state['idioma']
else:
    st.info('No ha seleccionado un idioma')
# st.dataframe(df_videos)

#intro_check = len(collect_df[collect_df['Name']=='Intro'])>0


categories = ['Ninguna','Canciones','Pops','Miscelaneas']
languages ={'Español':'ES','Portugués':'PT'}


def sample_without_consecutive_repeats(df, sample_size):
    sample = df.sample(sample_size, replace=True)
    sample =sample.reset_index(drop=True)
    # Check for consecutive repeated elements
    while any(sample.iloc[i]['Filename'] == sample.iloc[i+1]['Filename'] for i in range(len(sample)-1)):
        sample = df.sample(sample_size, replace=True)
        sample = sample.reset_index(drop=True)
    
    return sample

def rand_generator(numero):       
    intro_df = Promos_Intro_df[(Promos_Intro_df['Category']=='Intro') &(Promos_Intro_df['Language']==idioma)]
    try: 
        if repeat =='Si':
            sample = sample_without_consecutive_repeats(df, numero)
            conditions1 = [intro=='Si']
            conditions2 = [intro=='No']
        else: 
            sample =df.sample(numero,replace=False)
            conditions1 = [intro=='Si' , numero<=len(df)]
            conditions2 = [intro=='No' ,numero<=len(df)] 
        if all(conditions1):
            rand_df = pd.concat([intro_df,sample], ignore_index=True)
            return rand_df
        elif all(conditions2):
            rand_df = sample
            return rand_df
    except ValueError:
            st.error('El número de vídeos por colección no puede ser mayor al número de vídeos seleccionados.')
            

columnas = st.columns(2)
#video_type = col3.selectbox('Seleccione el tipo de video',)
#idioma = columnas[0].selectbox('Seleccione un idioma',languages.keys())
#if idioma:
#df = collect_df[(collect_df['Language']==idioma)]
num_collect = columnas[0].number_input('Establezca la cantidad de colecciones que desea',step=1, value=0, format="%d")
num_videos= columnas[1].number_input('Establezca la cantidad de videos de las colecciones',step=1,value=0, format="%d")
#else:
 #   st.info('Escoge un idioma')
promo_col, intro_col  = st.columns(2)
promo = promo_col.radio('Sus colecciones llevan promo',('No','Si'))
intro =intro_col.radio('Sus colecciones llevan introducción',('No','Si'))
#promo = st.radio('Sus colecciones llevan promo',('No','Si'))
#intro = st.radio('Sus colecciones llevan introducción',('No','Si'))
repeat =st.radio('Desea que algunos videos se repitan?',('No','Si'))
num_promo=0
if promo=='Si':
    num_promo=st.number_input('En que posición de la colecciones debe ir la promo',step=1,value=1,format="%d", max_value=num_videos+1)
    promo_dict ={'App':'Promo_App','Trailer': 'Promo_Trailer'} #,'Spotify':'Promo_Spotify'}
    la_promo= st.selectbox('Elija el tipo de promo para sus colecciones',promo_dict.keys())
    promos_df = Promos_Intro_df[(Promos_Intro_df['Category']== promo_dict[la_promo]) & (Promos_Intro_df['Language']==idioma)]
    #df[df['Category']=='Promo']
    #la_promo= st.selectbox('Elija la promo para sus colecciones',list(promos_df['Filename']))
    #la_promo = list(promos_df.sample(1)['Filename'])
sufijos = ['ra', 'da', 'ra', 'ta', 'ta', 'ta', 'ma', 'va', 'na', 'ma', 'va', 'ma', 'va',
 
                   'na', 'ma', 'va', 'ma', 'va', 'na', 'va']

def replace_duplicate_cols(df):
    cont =1
    df2= df 
    while cont > 0:
        for col in df.columns:
            for colu in df.drop(col, axis=1).columns:
                if all(df[col]==df[colu]): 
                    df2 = df.drop(col,axis=1)
        cont = len(df.columns)-len(df2.columns)
        if cont>0:
            for i in range(cont):
                new_df = rand_generator(num_videos)
                if intro=='Si':
                    fin_titulo = '_'.join(i for i in list(new_df['Name'][1:]))
                else:
                    fin_titulo = '_'.join(i for i in list(new_df['Name']))
                    titulo = f"COL_{num_videos}_{languages[idioma]}_{fin_titulo}"
                    df2[titulo] = new_df['Filename'].tolist()
        cont = len(df.columns)-len(df2.columns)
    return df2
    


if (num_collect > 0) & (num_videos>0):
    #tab_labels =[f'{str(i + 1) + sufijos[i]} Colección'  for i in range(num_collect)]
    lalist=[]
    promo_list=[]
    titulos = []
    i = 0
    while i<num_collect:
    # for i in range(num_collect):
        
        rand_df =rand_generator(num_videos)
        
        if intro=='Si':
            fin_titulo = '_'.join(i for i in list(rand_df['Name'][1:]))
        else:
             fin_titulo = '_'.join(i for i in list(rand_df['Name']))
             
        titulo = f"COL_{num_videos}_{languages[idioma]}_{fin_titulo}"
        
        # st.write(lalist)
        # st.write(any([titulo==item[0] for item in lalist]))
        # if not any([titulo==item[0] for item in lalist]): 
        if titulo not in titulos: 
            lalist.append([titulo] + rand_df['Filename'].tolist())
            if promo=='Si':
               promo_list.append(list(promos_df.sample(1)['Filename'])[0])
            i+=1   
            titulos = [titulo] + titulos
        

    
    df_final = pd.DataFrame(lalist)
    df_final = df_final.transpose()
    df_final.columns = df_final.iloc[0]
    df_final = df_final[1:]
    # df_final =  replace_duplicate_cols(df_final)
    if (len(promo_list)>0) & (intro=='No'):
        df_final = pd.concat([df_final.iloc[:num_promo-1], pd.DataFrame([promo_list], columns=df_final.columns),df_final.iloc[num_promo-1:]]).reset_index(drop=True)
    elif (len(promo_list)>0) & (intro=='Si'):
        df_final = pd.concat([df_final.iloc[:num_promo], pd.DataFrame([promo_list], columns=df_final.columns),df_final.iloc[num_promo:]]).reset_index(drop=True)
    else: pass 
    
    # if (num_promo  & (num_promo > 0)) & (intro=='Si'):
    #     df_final.loc[num_promo+1] = list(promos_df.sample(1)['Filename'])
    # elif (num_promo  & (num_promo > 0)) & (intro=='No'):
    #     df_final.loc[num_promo] = list(promos_df.sample(1)['Filename'])
    # else: 
    #     pass
    st.dataframe(df_final, use_container_width=True, hide_index=True)
    nombre_archivo =st.text_input('Escriba el nombre del archivo excel a crear (no hace falta la extensión)')
    creador =st.button('Crear Excel colecciones')
    if creador and nombre_archivo:
        
        st.session_state['collections_selected'] = df_final
        
        df_final.to_excel(f'\\\\cancer\\Material_Definitivo\\telerin\\COLECCIONES\\{nombre_archivo}.xlsx',index=False,header=True)
        st.success(f'Se ha creado el archivo excel con nombre {nombre_archivo}')
        st.success('Ubicado en' + r'\\' + '\\cancer\\Material_Definitivo\\telerin\\COLECCIONES')
       
else: st.info('Elija el número de colecciones')

