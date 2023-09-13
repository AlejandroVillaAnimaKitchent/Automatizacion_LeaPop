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

st.title("Catálogo de Miniaturas de Cuquines")

st.subheader('Escoge las miniaturas que quieras usar.')

df_cuquines = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\THUMBNAILS\00_Catálogo Miniaturas.xlsx', sheet_name=1, skiprows=3)


# selected = ['Tengo una muñeca vestida de azul', 'The Wheels on the bus 2',
#        'Un Elefante se Columpiaba', 'Vaca lechera',
#        'Vamos a Contar Mentiras', 'Vamos a la escuela',
#        'Vamos a la playa', 'Wheels on the bus colores']
selected = []

###################
# Functions define to perform a search on catalago_miniaturas
###################
# Using Google Translator we define 
def translate_text(text,language):
    translator = Translator()
    translation = translator.translate(text, dest=language)
    return translation.text

# Function to search for entries on the main df (individual videos)

def search_entries(df, word):
    sub_df =pd.DataFrame(columns = df.columns)
    languages =['spanish','portuguese','english']
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
    palabra =st.text_input('Ingrese una palabra clave de la miniatura que desea buscar : ')
    if palabra:
        df = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv')
        df = df[(df['Components']==1)& (df['Activo']=='Si')]
        df_videos = search_entries(df,palabra)
        selected =  list(df_videos.Name.unique())    
    
if len(selected)==0:
    cuquines = df_cuquines[~df_cuquines.Miniatura_01.isna()].reset_index(drop=True)
else:
    cuquines = df_cuquines[(~df_cuquines.Miniatura_01.isna()) & (df_cuquines['Title Spanish'].isin(selected))].reset_index(drop=True)
    
cuqs = cuquines['Title Spanish'].values
df_sliced = cuquines.iloc[:, 1:21] 
df_dict = df_sliced.apply(lambda row: row.dropna().values, axis=1).to_dict()
new_dict = {values[0]: list(values[1:]) for values in df_dict.values()}

thumbs_by_cuquin = {}
cuq_thumb_dict = {}

# Cuquines
for cuq_silce in generate_slices(len(cuqs)):
    cuqtabs = st.tabs(list(cuqs)[cuq_silce])
    con_minis = df_sliced.apply(lambda row: row.dropna().values, axis=1)[cuq_silce]
    for tab_index in range(len(cuqtabs)):
        with cuqtabs[tab_index]: 
            mini_list = []
            with st.expander("Desplegar"):
                st.header(cuqs[tab_index+cuq_silce.start])
                num_thumbs = len(con_minis[tab_index+cuq_silce.start])-1
                num_rows = (num_thumbs//4)+1
                for row in range(num_rows):
                    cols = st.columns(4, gap='medium')
                    sub_cols = 4 if row+1<num_rows else num_thumbs%4
                    for i in range(sub_cols):
                        with cols[i]:
                            num = row*4 + i +1 
                            image = con_minis[tab_index+cuq_silce.start][num]
                            st.image(r"\\cancer\Material_Definitivo\telerin\THUMBNAILS\lowres\{}".format(image))
                            agree = st.checkbox("{}".format(image.replace('.png','')),key=cuqs[tab_index+cuq_silce.start]+str(row)+str(i)+'_')
                            mini_list.append(agree) 
                            # st.session_state['song_thumb_list'].append(agree)
        cuq_thumb_dict[cuqs[tab_index+cuq_silce.start]]=mini_list
                            
     
if st.sidebar.button('Guardar selección de cuquines'):
    for key in new_dict:
        thumbs_by_cuquin[key] = list(compress(new_dict[key],cuq_thumb_dict[key]))
    st.session_state['thumbs_by_cuquin'] = thumbs_by_cuquin

    