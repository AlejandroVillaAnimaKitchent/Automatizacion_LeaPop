# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 16:32:54 2023

@author: alejandro.villa
"""

#We call All the DB from the folder \\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase
import pandas as pd 
import re 


  
cuquines =pd.read_excel( r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Cuquines_DB.xls')
canciones = pd.read_excel(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Canciones_DB.xls')
promos = pd.read_excel(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Promos_DB.xls')
miscelaneas =pd.read_excel(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Miscelaneas_DB.xls')
individuales_y_colecciones =pd.read_csv(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv')

def update_ind_col():
    global individuales_y_colecciones
    name_pattern = r"(?<=(_EN_|_ES_|_PT_))(.*)(?=(.mp4))"
    cuquines =pd.read_excel( r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Cuquines_DB.xls')
    canciones = pd.read_excel(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Canciones_DB.xls')
    promos = pd.read_excel(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Promos_DB.xls')
    miscelaneas =pd.read_excel(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Miscelaneas_DB.xls')
    dfs= [cuquines,canciones,promos,miscelaneas]
    individuales_y_colecciones =pd.read_csv(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv')
    los_dict=[]
    for df in dfs:
        for k,new_path in enumerate(df['Path']):
            if new_path not in individuales_y_colecciones['Path'].tolist():
                aux_dict ={key: None for key in individuales_y_colecciones.columns}
                aux_dict['Path']=df['Path'][k]
                aux_dict['Filename']=df['Nombre_Archivo'][k]
                aux_dict['Components']= df['Componentes'][k]
                aux_dict['Type']= 'Individual' if  aux_dict['Components']==1 else 'Collection'
                aux_dict['Characters']= 'Cleo & Cuquin' if df['videos_string'][k].startswith('CC') else 'Unspecified'
                aux_dict['Tag_IP']= 'IP_FT' if aux_dict['Characters']== 'Cleo & Cuquin' else  None
                aux_dict['Language'] = 'Español' if '_ES_' in df['Nombre_Archivo'][k]  else ('Inglés' if '_EN_' in df['Nombre_Archivo'][k] else 'Portugués')
                aux_dict['Category'] = 'Music' if df is canciones else ('Education' if df is cuquines else ('Promo' if df is promos else 'Unspecified')) 
                aux_dict['Name'] =df['Nombre_Archivo'].apply(lambda x: re.search(name_pattern, x).group(1).replace('_', ' ') if re.search(name_pattern, x) else '')
                los_dict.append(aux_dict)
    aux_df =pd.DataFrame(los_dict)
    individuales_y_colecciones = pd.concat([individuales_y_colecciones,aux_df],ignore_index=True)
    individuales_y_colecciones.to_csv(r'\\PEGASO\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Individual_y_Colecciones.csv',index=False)

    
    