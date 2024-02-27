import streamlit as st
import pandas as pd
from itertools import compress
from googletrans import Translator

def generate_slices(n):
    return [slice(i, min(i + 6, n)) for i in range(0, n, 6)]
    

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     

st.title("Catálogo de Miniaturas de Canciones")

st.subheader('Escoge las miniaturas que quieras usar.')

df_canciones = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Miniaturas_LeaPop.csv')
df_canciones =df_canciones[df_canciones['Category']=='Music']

selected = []
###################
# Functions define to perform a search on Miniaturas_LeaPop

###################
# Using Google Translator we define 

def translate_text(text,language):
    translator = Translator()
    translation = translator.translate(text, dest=language)
    return translation.text

# Function to search for entries on the main df (individual videos)

def search_entries(df, word):
    sub_df =pd.DataFrame(columns = df.columns)
    languages =['spanish','portuguese']
    for language in languages:
        try:
            search_word = translate_text(word,language)
            mask = df['Name'].str.contains(search_word, case=False) | df['Name_Language'].str.contains(search_word, case=False) | df['Filename'].str.contains(search_word, case=False)
            if len(df[mask])>0: sub_df =pd.concat([sub_df,df[mask]],ignore_index=True)
            else: pass 
        except: pass
    return sub_df


if 'selected_videos' in st.session_state:
    df_videos = st.session_state['selected_videos']
    selected = list(st.session_state['selected_videos'].Name.unique())
    # st.text(selected[0])
else:
    st.info('No hay vídeos seleccionados')    
    palabra =st.text_input('Ingrese una palabra clave de la miniatura que desea buscar : ')
    if palabra:
        df = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_Colecciones_LeaPop.csv')
        df = df[(df['Components']==1)& (df['Activo']=='Si')]
        df_videos = search_entries(df,palabra)
        selected =  list(df_videos.Name.unique())
    
    
if len(selected)==0:
    canciones = df_canciones[~df_canciones.Miniatura_01.isna()].reset_index(drop=True)
else:
    canciones = df_canciones[(~df_canciones.Miniatura_01.isna()) & (df_canciones['Title Spanish'].isin(selected))].reset_index(drop=True)
    # st.text(len(canciones))
songs = canciones['Title Spanish'].values
df_sliced = canciones.iloc[:, 1:21] 
df_dict = df_sliced.apply(lambda row: row.dropna().values, axis=1).to_dict()
new_dict = {values[0]: list(values[1:]) for values in df_dict.values()}

thumbs_by_song = {}
song_thumb_dict = {}


# Canciones
for song_slice in generate_slices(len(songs)):
    songtabs = st.tabs(list(songs)[song_slice])
    con_minis = df_sliced.apply(lambda row: row.dropna().values, axis=1)[song_slice]
    for tab_index in range(len(songtabs)):
        mini_list = []
        with songtabs[tab_index]:
            with st.expander("Desplegar"):
                st.header(songs[tab_index+song_slice.start])
                num_thumbs = len(con_minis[tab_index+song_slice.start])-1
                num_rows = (num_thumbs//4)+1
                for row in range(num_rows):
                    cols = st.columns(4, gap='medium')
                    sub_cols = 4 if row+1<num_rows else num_thumbs%4
                    for i in range(sub_cols):
                        with cols[i]:
                            num = row*4 + i +1 
                            image = con_minis[tab_index+song_slice.start][num]
                            st.image(r"\\cancer\Material_Definitivo\LEA\COLECCIONES\Thumbs\lowres\{}".format(image))
                            agree = st.checkbox("{}".format(image.replace('.png','')),key=songs[tab_index+song_slice.start]+str(row)+str(i)+'_')
                            mini_list.append(agree) 
        song_thumb_dict[songs[tab_index+song_slice.start]]=mini_list
                            
     
if st.sidebar.button('Guardar selección de canciones'):
    for key in new_dict:
        thumbs_by_song[key] = list(compress(new_dict[key],song_thumb_dict[key]))
    st.session_state['thumbs_by_song'] = thumbs_by_song

