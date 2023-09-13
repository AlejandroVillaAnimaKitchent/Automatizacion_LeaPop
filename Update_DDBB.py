# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 09:40:12 2023

@author: alejandro.villa
"""

import pandas as pd 
import re 


#All the DDBB 

ind_col = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv')
cuquines = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Cuquines_DB.xls')
canciones = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Canciones_DB.xls')
promos = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Promos_DB.xls')
miscelaneas = pd.read_excel( r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Miscelaneas_DB.xls')
contador_colecciones = pd.read_csv( r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Contador_colecciones.csv')
canciones_sueltas = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Canciones_Sueltas.csv')
colecciones = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Colecciones.csv')
promos_intros = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Promos_Intros.csv')
listado_comercial_cc = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\listado_comercial_cc.csv')
listado_comercial_cq = pd.read_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\listado_comercial_cq.csv')


#We Define the functions to Update all the DataBases 


##############################################
#Updates all the sub-DB that depend on ind_col 

def easy_updates():
    
    #Promos Intros 
    promos_intros = ind_col[((ind_col['Components']==1)& ind_col['Category'].isin(['Promo_App','Promo_Trailer','Promo_Spotify'])) | (ind_col['Category']=='Intro')]
    promos_intros.to_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Promos_Intros.csv')
    
    #Cacnciones Sueltas 
    canciones_sueltas =ind_col[ind_col['Components']==1]
    canciones_sueltas.to_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Canciones_Sueltas.csv')
    
    #Colecciones
    colecciones = ind_col[ind_col['Components']>1]
    colecciones.to_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Colecciones.csv')
  
##############################################


##############################################################################

#The Main Update which is The  ind_col DDBB


def update_ind_col():
    los_dict=[]
    name_pattern = r"(?<=(_EN_|_ES_|_PT_))(.*)(?=(.mp4))"
    dfs = [cuquines,canciones,promos,miscelaneas]
    los_paths = ind_col['Path'].tolist()
    for df in dfs:
        for k,new_path in enumerate(df['Path']):
            if new_path not in los_paths:
                los_paths.append(new_path)
                aux_dict ={key: None for key in ind_col.columns}
                aux_dict['Path']=df['Path'][k]
                aux_dict['Filename']=df['Nombre_Archivo'][k]
                aux_dict['Components']= df.iloc[k].count()-4 if pd.isna(df['Tag'].iloc[k]) else df.iloc[k].count()-5
                aux_dict['Type']= 'Individual' if  aux_dict['Components'] ==1 else 'Collection'
                aux_dict['Characters']= 'Cleo & Cuquin' if df['videos_string'][k].startswith('CC') else 'Unspecified'
                aux_dict['Tag_IP']= 'IP_FT' if aux_dict['Characters']== 'Cleo & Cuquin' else  None
                aux_dict['Language'] = 'Español' if '_ES_' in df['Nombre_Archivo'][k]  else ('Inglés' if '_EN_' in df['Nombre_Archivo'][k] else 'Portugués')
                aux_dict['Category'] = (
                                        'Music' if df is canciones else
                                        'Education' if df is cuquines else
                                        ('Promo_App' if df['Nombre_Archivo'].str.contains('APP', case=False ).any() else
                                         'Promo_Trailer' if df['Nombre_Archivo'].str.contains('Trailer', case=False).any() else
                                         'Promo_Spotify' if df['Nombre_Archivo'].str.contains('Spotify',case=False).any() else
                                         'Unspecified')
                                        )
                aux_dict['Name'] = re.search(name_pattern, df['Nombre_Archivo'].iloc[k] ).group(0).replace('_', ' ') if re.search(name_pattern, df['Nombre_Archivo'].iloc[k]) else ''
                aux_dict['Activo'] ='Si'
                aux = pd.Series(df.iloc[k])
                aux.drop(['videos_string', 'Path', 'Nombre_Archivo', 'Tag', 'Componentes'],inplace=True)
                aux.dropna(inplace=True)
                aux = [item.strip() for element in ind_col[ind_col['Filename'].isin(aux.tolist())]['Tag_pieza'].tolist() for item in element.split('|')]
                aux_dict['Tag_pieza'] = '|'.join(set(aux))
                los_dict.append(aux_dict)
    aux_df =pd.DataFrame(los_dict)
    otra_df = pd.concat([ind_col, aux_df],ignore_index=True)
    otra_df.to_csv(r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv')  


##############################################################################


#Now we actually update all the dataBases THE ORDER IS VERY IMPORTANT 

update_ind_col() 

easy_updates()
