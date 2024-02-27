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

st.title("Catálogo de Miniaturas de Pops")

st.subheader('Escoge las miniaturas que quieras usar.')

df_pops = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Miniaturas_LeaPop.csv')
df_pops = df_pops[df_pops['Category']=='Education']


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
        df = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_Colecciones_LeaPop.csv')
        df = df[(df['Components']==1)& (df['Activo']=='Si')]
        df_videos = search_entries(df,palabra)
        selected =  list(df_videos.Name.unique())    
    
if len(selected)==0:
    pops = df_pops[~df_pops.Miniatura_01.isna()].reset_index(drop=True)
else:
    pops = df_pops[(~df_pops.Miniatura_01.isna()) & (df_pops['Title Spanish'].isin(selected))].reset_index(drop=True)
    
poppies = pops['Title Spanish'].values
df_sliced = pops.iloc[:, 1:21] 
df_dict = df_sliced.apply(lambda row: row.dropna().values, axis=1).to_dict()
new_dict = {values[0]: list(values[1:]) for values in df_dict.values()}

thumbs_by_pop = {}
pop_thumb_dict = {}

# Pops
for pop_silce in generate_slices(len(poppies)):
    poptabs = st.tabs(list(poppies)[pop_silce])
    con_minis = df_sliced.apply(lambda row: row.dropna().values, axis=1)[pop_silce]
    for tab_index in range(len(poptabs)):
        with poptabs[tab_index]: 
            mini_list = []
            with st.expander("Desplegar"):
                st.header(poppies[tab_index+pop_silce.start])
                num_thumbs = len(con_minis[tab_index+pop_silce.start])-1
                num_rows = (num_thumbs//4)+1
                for row in range(num_rows):
                    cols = st.columns(4, gap='medium')
                    sub_cols = 4 if row+1<num_rows else num_thumbs%4
                    for i in range(sub_cols):
                        with cols[i]:
                            num = row*4 + i +1 
                            image = con_minis[tab_index+pop_silce.start][num]
                            st.image(r"\\cancer\Material_Definitivo\LEA\COLECCIONES\Thumbs\lowres\{}".format(image))
                            agree = st.checkbox("{}".format(image.replace('.png','')),key=poppies[tab_index+pop_silce.start]+str(row)+str(i)+'_')
                            mini_list.append(agree) 
                            # st.session_state['song_thumb_list'].append(agree)
        pop_thumb_dict[poppies[tab_index+pop_silce.start]]=mini_list
                            
     
if st.sidebar.button('Guardar selección de cuquines'):
    for key in new_dict:
        thumbs_by_pop[key] = list(compress(new_dict[key],pop_thumb_dict[key]))
    st.session_state['thumbs_by_pop'] = thumbs_by_pop

    