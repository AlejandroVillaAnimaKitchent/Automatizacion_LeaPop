#Libraries 
#############################################################################################################################
import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta, time
import random
import numpy as np
#############################################################################################################################


#We create the page's style  
#############################################################################################################################
st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)  

#############################################################################################################################
   

#ALL DATABASES NEEDED 
##############################################################################################################################

# Colecciones  

collect_df =pd.read_csv(r"\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_Colecciones_LeaPop.csv")
##################################################################################### 
#Channels to include Provisionary solution

csv_file = df_channel = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\canales_excel_yt.csv')

##################################################################################### 
channels = df_channel.set_index('Título del canal')['Canal'].to_dict()
channels_cont = pd.read_csv(r"\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Contador_colecciones.csv")     
categories = ['Music','Education']
languages ={'Español':'ES','Portugués':'PT'}
Promos_Intro_df = pd.read_csv(r"\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Promos_Intro_LeaPop.csv")

#####################################################################################
# Dictionary of Thumbnails 

df_thumbs = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Miniaturas_LeaPop.csv')
df_thumbs = df_thumbs.drop(df_thumbs.columns[[0]], axis=1)
#df_dict = df_thumbs.apply(lambda row: row.dropna().values, axis=1).to_dict()
#all_thumbs = {values[0]: list(values[1:]) for values in df_dict.values()}
    
##################################################################################### 
# Tags and descriptions 

tags_description = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Tags_LeaPop.csv')

#############################################################################################################################


#WE WILL DEFINE ALL THE FUNCTIONS TO BE USED IN CREATING THE EXCEL FILE FOR YOUTUBE
#############################################################################################################################

#FUNCTION TO CREATE THE all_thumbs dictionary using only the selected videos
############################
def df_dictionary(selected_videos):
    global df_thumbs, df_dict
    df_thumbs = df_thumbs[df_thumbs['Title Spanish'].isin(selected_videos.Name)]
    df_dict = df_thumbs.apply(lambda row: row.dropna().values, axis=1).to_dict()
    return  {values[0]: list(values[1:]) for values in df_dict.values()}
############################


#FUNCTION THAT CREATES THE DATABASE WITH JUST THE DATA NEEDED 
##########################
def filenames_fun(category_chosen,idioma):
    return collect_df.loc[(collect_df['Language']==idioma) & (collect_df['Category']==category_chosen),['Filename','Name','Components','Tag_IP','Tag_pieza']]   
##########################

#FUNCTION TO CONCATENATE THE LIST TO BE ABLE TO REPEAT VIDEOS IF NECESSARY 
#########################
def concatenate_list(lista,len_otra_lista): 
    repetitions = len_otra_lista // len(lista)
    remaining_slots = len_otra_lista % len(lista)
    new_list = lista*repetitions +lista[:remaining_slots]
    return new_list
#########################

#FUNCTION TO CHOOSE THE PARAMETERS NEEDED FOR THE CREATION OF THE EXCEL FILE 
##########################
def parameter_choice():
    global channel_choice, idioma, category_chosen, lengua
    global videos_df, titles_df, labels_df
    global thumbs_by_song, thumbs_by_cuquin

    
    channel_choice = st.selectbox("Seleccione un canal", sorted(list(channels.keys())))
    col1,col2 =st.columns(2)
    category_chosen = col1.selectbox('Seleccione una categoria',categories)
    idioma = col2.selectbox('Seleccione el idioma de sus vídeos',languages.keys())
    lengua = st.radio('Desea que los títulos y las descripciones de sus vídeos sean en inglés',('No','Si'))
##########################
    
 
#FUNCTION TO REQUEST THE DAY AND  HOURS  OF PUBLICATION
##########################       
def time_request():
    global selected_date, horas, horas_df, length_df 
    horas_df=list()
    sufijos = ['er', 'do', 'er', 'to', 'to', 'to', 'mo', 'vo', 'no', 'mo', 'vo', 'mo', 'vo',
               'no', 'mo', 'vo', 'mo', 'vo', 'no', 'vo']
    st.write('A continuación se establecerá el calendario de publicación: fecha de inicio, cadencia de vídeos y horas de publicación.')
    selected_date = st.date_input("Seleccione la fecha inicial publicación")
    dias = st.number_input('Establezca la cantidad de días que desea publicar', step=1,value=1,format="%d")
    num_cols = int( st.number_input('Establezca la cantidad de videos por día',step=1, value=0, format="%d"))
    length_df = dias*num_cols
    try:   
        st.write('Seleccione  EN ORDEN los horarios de publicación')
        cols = st.columns(num_cols)
        default_time = time(0, 0)
        horas = [col.time_input(f'Seleccione el {str(cols.index(col)+1)+ sufijos[cols.index(col)] }  horario de publicación',default_time, key=cols.index(col)) for col in cols]
        i=0
        while i < length_df:
            
            if i>1 and i%len(horas)==0: selected_date += timedelta(days=1)
            time_str = datetime.combine(selected_date, horas[i % len(horas)]).strftime("%Y-%m-%dT%H:%M:%SZ")
            horas_df.append(time_str)
            i+=1
            
    except:
        pass
##########################
    
#Function designed to request the selection of keywords from a lake of keywords used in the past by the team.
#########################
def keywords_request():
    
    global tag_musical, tag_educativo, tag_general, keywords_dict, keywords_df
    
    keywords=list()
    tag_musical =[]
    tag_general =[]
    tag_educativo =[]
    keywords_dict ={}
    
    ################################################
    Tags_Music ='Tags_Music_'+languages[idioma]
    Tags_General ='Tags_General_'+languages[idioma]
    Tags_Educativo ='Tags_Educativo_'+languages[idioma]
    
    tag_musical = tags_description[Tags_Music].dropna().tolist()
    tag_general = tags_description[Tags_General].dropna().tolist()
    tag_educativo =tags_description[Tags_Educativo].dropna().tolist()
    
    if category_chosen =='Music':
        keywords_dict = { tag : tag for tag  in tag_musical + tag_general}
    elif category_chosen =='Education':
        keywords_dict = { tag : tag for tag  in tag_educativo + tag_general}
     #################################################

            
    #################################################   
           
    keywords = list(keywords_dict.keys())
        
    key_words = list()
    st.write('Los vídeos incluirán tags predeterminadas, pero puedes añadir más a continuación.')
    num_cols = 4
    num_ros = math.ceil(len(keywords) / num_cols)
    for ro in range(num_ros):
        ro_items = keywords[ro*num_cols: (ro+1)*num_cols]
        cols = st.columns(num_cols)
        for cols_idx, items in enumerate(ro_items):
            checkbox_sta = cols[cols_idx].checkbox(items,key=items + str(cols_idx) +str(ro_items))
            if checkbox_sta:
                key_words.append(items)
                
    key_words = [keywords_dict[x] for x in key_words]

    words = st.text_input('Escriba alguna(s) palabra(s) adicional(es) si así lo desea (separadas por comas).')
    if words:
        keywords_df = words +','+','.join(str(i) for i in key_words)
    else:
        keywords_df = ','.join(str(i) for i in key_words)
    #########################        
    
###############################################################################################
        
# #FUNCTION TO CREATE THE TITLES OF THE VIDEOS  VERSION 2.0 
###############################################################################################

def create_titles():
    
    global titles_df
    
    double_title= st.radio('Desea usar el título del primer y segundo vídeo de la colección',('No','Si'))
    
    ############### To take the titles of a given video ###############
    #titles_to_use =['Name_Language', 'Second_Name_Language','Third_Name_Language','Fourth_Name_Language']
    titles_to_use =['Name_Language']
    titles_file = lambda Filename: list(collect_df.loc[collect_df['Filename']==Filename][titles_to_use].dropna(axis=1).values[0])
    ###################################################################
    
    ############### To Drop the Intro and/or Promos rows ###############
    collec = collections_selected[~collections_selected.apply(lambda row: row.isin(Promos_Intro_df['Filename'])).any(axis=1)]
    collec= collec.reset_index(drop=True)
    ####################################################################
    
    ########### Number of collections given ###########
    num_collect = len(list(collec.columns))
    ###################################################
    
    ############### Scalable to more titles if needed ###############
    if double_title =='Si': 
        if len(collec)>1: upper_limit = 2
        else: 
            upper_limit = 1  
            st.text('Solo hay una componente por colección, se procederá con los títulos para esta ÚNICA componente')
    else: upper_limit = 1   
    ################################################################
    
    ####### Creates a list of title per row in collec (collecttions_selected without intro/promos) #######     
    lista_posiciones =[collec.iloc[i].tolist() for i in range(upper_limit)]

    titulos_por_fila =[]

    for i in range(upper_limit):
        lista_titulos = []
        lista_videos = lista_posiciones[i]
    
        for index ,video in enumerate(lista_videos):
            title_names = titles_file(video) 
            indice = (lista_videos[:index].count(video))%len(title_names)
            lista_titulos.append(title_names[indice])
    
        titulos_por_fila.append(lista_titulos)
    #######################################################################################################
    
    ############ Creates the list of titles per position (1st Title,2nd title, etc) ############ 
    Titulos =[]
    for i in range(num_collect):
        title=''
        j=0
        while j <upper_limit:
            if title =='': 
                title = titulos_por_fila[j][i] 
                j+=1
            
            else:
                if len(title + ' | '+ titulos_por_fila[j][i])>=100:
                    break
                else:
                    title += ' | '+ titulos_por_fila[j][i]
                    j+=1
        Titulos.append(title)
    ############################################################################################
    
        
    #To ask for addtional phrases for the titles and list them to coincide with the total of vidoes available. 
    #########################
    sufijos= ['era', 'da', 'era', 'ta', 'ta', 'ta', 'ma', 'va', 'na', 'ma',
                         'va', 'ma', 'va', 'na', 'ma', 'va', 'ma', 'va', 'na', 'va']  #Sufixes for spanish 'til #20
    num_cols = int( st.number_input('Establezca la cantidad de frases adicionales que acompañaran sus títulos',step=1, value=0, format="%d"))
    try: 
        cols = st.columns(num_cols)
        words = [' ' + col.text_input(f'Escriba la {str(cols.index(col)+1)+ sufijos[cols.index(col)]} frase', key=50+num_cols +cols.index(col)) for col in cols]
    except:
        words=[' ']
        st.info('Va a proceder con los títulos de los vídeos sin frases adicionales.')

    
    wors = concatenate_list(words,num_collect)
    #########################
    
    ############ Creates the final Titles list for the DF ############
    titles_df = [Titulos[i]+wors[i] if len(Titulos[i]+wors[i])<100 else Titulos[i] for i in range(num_collect)]
    ################################################################## 


###############################################################################################
       
#FUNCTION TO CREATE THE DESCRIPTIONS OF THE VIDEOS 
#########################
def create_descs():
    global desc_df
    descriptions = []
    st.write('Elija una(s) descripción(es) para sus vídeos y/o escribala(s)')
    
    #################################################  
    Description ='Description_'+languages[idioma]
    
    descriptions =  tags_description[Description].dropna().tolist()
    
    descriptions_dict ={ description : description for description in descriptions}
    #################################################
        

    desc = str()
    
    for i, des in enumerate(descriptions):
        la_box = st.checkbox(des, key=i + len(str(des)))
        if la_box:
            desc += descriptions_dict[des] + ' '
            
    des = st.text_input('Escriba un complemento a las descripciones escogidas (o su propia descripción si no ha elegido ninguna) para todos los vídeos')
    if des:
        desc += ' ' + des
    else:
        pass
    desc_df = [desc for col in  collections_selected.columns]
#########################

###############################################################################################
      
#FUNCTION TO CREATE THE FINAL DF THAT WILL BE USED TO CREATE THE EXCEL 
##########################
def create_df():
    df=pd.DataFrame(columns=['filename','channel','custom_id','add_asset_labels','title','description',
                             'keywords','spoken_language','caption_file','caption_language','category','privacy','notify_subscribers','start_time','end_time',
                             'custom_thumbnail','ownership','block_outside_ownership','usage_policy','enable_content_id','reference_exclusions','match_policy',
                             'ad_types','ad_break_times','playlist_id','is_made_for_kids'])
    
    ##############################################
    #Very Important for videos_df assigment to be first
    df['filename']= concatenate_list([item+'.mp4' for item in collections_selected.columns])
    ##############################################
    df['channel'] = channels[channel_choice]
    df['category'] = category_chosen
    df['spoken_language'] = languages[idioma]
    df['ownership']='WW'
    df['usage_policy'] ='Monetize in all countries'
    df['enable_content_id'] ='no'
    df['is_made_for_kids'] ='yes'
    df['title']= concatenate_list(titles_df,length_df)
    df['description']= concatenate_list(desc_df,length_df)
    df['keywords'] = keywords_df
    df['keywords'] = df['keywords'].str.replace(',','|')
    df['start_time']= horas_df
    thumbs_labels_creator()
    df['add_asset_labels'] = concatenate_list(asset_labels,length_df)
    df['custom_thumbnail'] = concatenate_list(custom_thumbs,length_df)
    st.dataframe(df)
    return df
##########################


#FUNCTION TO ASK FOR A FILE IF CREADOR ALEATORIO DE COLECCIONES WAS NOT USED 
##########################
def ask_file():
    global  videos_df, collections_selected, selected_videos, thumb_dict, asset_labels, all_thumbs
    file = st.file_uploader("Suba el Archivo Excel de sus colecciones", type=["xlsx", "xls","ods"])
    if file: 
        collections_selected = pd.read_excel(file)
        #VAMOS a crear todos los datasets necesarios 
        
        #selected_videos  and videos_df 
        videos_list = []
        for i in range(len(collections_selected.columns)):
            column_values = collections_selected.iloc[:, i].unique().tolist()
            videos_list.extend(column_values)
        videos_list = list(set(videos_list))
        selected_videos = collect_df[(collect_df['Filename'].isin(videos_list)) & (collect_df['Components']==1)]
        videos_df = selected_videos.Name
        
        all_thumbs =  df_dictionary(selected_videos)
        
        thumb_dict ={}
        for Name in videos_df: 
            
            if 'promo' not in str.lower(Name):
                related_thumbs = df_thumbs[df_thumbs['Title Spanish'] == Name]
                
                try:
                    non_na_thumbs = related_thumbs.stack().dropna().tolist()
                    #st.write(Name)
                    #st.write(non_na_thumbs)
                    thumb_dict[non_na_thumbs[0]] =non_na_thumbs[1:] 
                except: 
                    st.error("CUIDADO !!!!!! NO PROCEDA")
                    st.error("Para el video '{}' No se encontraron Thumbs".format(Name))
                    st.error('Consulte a su programador de confianza.')
                
                
        # Los Tags 
        asset_labels = []
    
        for col in collections_selected.columns:
            videos = [video for video in collections_selected[col] if video not in list(Promos_Intro_df['Filename'])]
            tags_IP = []
            tags_pieza = []
            # st.text(videos)
            for video in videos:

                ips_ = list(selected_videos[selected_videos.Filename==video].Tag_IP.values)[0]
                ips = ips_.split('|')
                
                tags_pieza = list(selected_videos[selected_videos.Filename==video].Tag_pieza.values)
                piezas_ = tags_pieza[0] if len(tags_pieza)>0 else ''
    
                if isinstance(piezas_, str):
                    piezas = piezas_.split('|') if piezas_ != '' else []
                else:
                    piezas = [] if np.isnan(piezas_) else [piezas_]

                tags_IP += ips
                tags_pieza += piezas
            asset_labels.append('|'.join(list(set(tags_IP+tags_pieza))))
##########################

##########################
def No_file(): 
    global  videos_df, collections_selected, selected_videos, thumb_dict
##########################
    

#FUNCTION TO CREATE THUMBS AND LABELS LIST 
##########################
def thumbs_labels_creator(): 
    global custom_thumbs, asset_labels
    custom_thumbs = []

    for j in range(length_df):
        col = collections_selected.columns[j%len(collections_selected.columns)]
        if len(thumb_dict.keys())>0:
                videos = [video for video in collections_selected[col] if video not in list(Promos_Intro_df['Filename'])]
                videofilename = videos[0]
                video = selected_videos[selected_videos.Filename==videofilename]['Name'].values[0]
                if len(thumb_dict[video])>0:
                    custom_thumbs.append(random.choice(thumb_dict[video]))
                else:
                    custom_thumbs.append(random.choice(all_thumbs[video]))
        else:
            for col in collections_selected.columns:
                videos = [video for video in collections_selected[col] if video not in list(Promos_Intro_df['Filename'])]
                videofilename = videos[0]
                video = selected_videos[selected_videos.Filename==videofilename]['Name'].values[0]
                custom_thumbs.append(random.choice(all_thumbs[video]))
##########################
    

           

#DEPLOYMENT THE APP USING ALL THE PREVIOUSLY DEFINED FUNCTIONS, DATAFRAMES AND DICTIONARIES.
#############################################################################################################################

###########################################
def main():
    global videos_df, collections_selected, selected_videos, thumb_dict, asset_labels, all_thumbs
    
    st.title('Creador de Hoja de Cálculo para Canal Youtube')
    
    if 'collections_selected' in st.session_state:
        radio_index = 0
    else:
        radio_index = 1
    
    #####################################################################################
    #We ask the user if it has it's own file or wants to use the just created Collection
    file_or_not = st.radio('Desea usar la colección creada en la pestaña anterior',('Si','No'), index=radio_index)
    #####################################################################################
    missing = []
    try:
        selected_videos = st.session_state['selected_videos']
        videos_df = selected_videos.Name
        
        all_thumbs =  df_dictionary(selected_videos)
    except:
        missing.append('vídeos')
       
    try:
        collections_selected = st.session_state['collections_selected']
    except:
        missing.append('colecciones')
        
    if len(missing)>0 and radio_index == 0:
        if len(missing) == 1:
            st.info("Faltan {} por escoger.".format(missing[0]))
        else:
            st.info("Faltan {} y {} por escoger.".format(missing[0],missing[1]))

    try:
        thumbs_by_song = st.session_state['thumbs_by_song']
    except:
        thumbs_by_song = {}

    try:
        thumbs_by_pop = st.session_state['thumbs_by_pop']
    except:
        thumbs_by_pop = {}

    #CREATING THE LISTS WITH THUMB PATH'S AND LABELS OF EVERY VIDEO.      


    thumb_dict = thumbs_by_song|thumbs_by_pop
    
    #If The user wants to utilize the collection previously done:
    No_file() 
    if file_or_not =='Si': 
        asset_labels = []
    
        for col in collections_selected.columns:
            videos = [video for video in collections_selected[col] if video not in list(Promos_Intro_df['Filename'])]
            tags_IP = []
            tags_pieza = []
            #st.text(videos)
            for video in videos:
                ips_ = list(selected_videos[selected_videos.Filename==video].Tag_IP.values)[0]
                #st.write(video)
                # st.write(ips_)
                ips = ips_.split('|')
                
                piezas_ = list(selected_videos[selected_videos.Filename==video].Tag_pieza.values)[0]
                #st.write(piezas_)
                piezas = piezas_.split('|')
                tags_IP += ips
                tags_pieza += piezas
            asset_labels.append('|'.join(list(set(tags_IP+tags_pieza))))
    
    #If not, we ask for a local file to be uploaded. 
    
    elif file_or_not =='No': ask_file()
    
    # Header and everything else
    
    st.subheader('Escoge los parámetros con los cuáles desea crear la hoja de Cálculo')
    parameter_choice()
    keywords_request()
    time_request()
    conditions =[False,False,False,False]
    try:
        create_titles()
        create_descs()
        
        conditions = [list(videos_df), category_chosen != 'Ninguna', idioma != 'Ninguno',keywords_df,horas_df]
        
        if all(conditions):
            df=create_df()
            if st.button('Crear Hoja De Cálculo'):
            
                index = channels_cont[channels_cont['Título del canal'] ==channel_choice].index[0]
                channels_cont.loc[index,'Contador colecciones'] +=1
                col_number =channels_cont.loc[index,'Contador colecciones']
                channels_cont.to_csv(r"\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Contador_colecciones.csv", index=False)
                channel_choice_windows = channel_choice.replace(':','').replace('!','') # Omit dangerous characters for file naming.
                file_path = f'\\\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\\Youtube_Excels\\{channel_choice_windows}_{col_number}.xlsx'
    
                try:
                    df.to_excel(file_path, header=True, index=False, engine='xlsxwriter')
                    st.success(f'Se ha creado el archivo {channel_choice_windows}_{col_number}.xlsx  en la ubicación')
                    st.success(r'\\'+f'\\cancer\\Material_Definitivo\\LEA\\COLECCIONES\\ Lea&Pop Databases\\Youtube_Excels\\{channel_choice_windows}_{col_number}.xlsx')
                except Exception as e:
                    st.error(e)
        else:
           st.error('Recuerde elegir todas las opciones.')
           if conditions[1]==False: 
               st.info('Deber elegir una categoría para tu canal.')
           elif conditions[2]==False:
               st.info('Debes elegir un idioma para tu canal.')
           elif len(keywords_df) ==0:
               st.info('Debes elegir keywords para los videos de tu canal.')
           elif  len(horas_df)==0:
               st.info('Debes elegir horarios para los videos de tu canal.')
          
               
               
           
    except Exception as e:
        print(e)
        st.info('Necesitas añadir un excel o eleger colecciones de vídeos mediante las pestañas anteriores.')
###########################################

#############################################################################################################################

#############################################################################################################################
if __name__ == "__main__":

   main()
#############################################################################################################################
