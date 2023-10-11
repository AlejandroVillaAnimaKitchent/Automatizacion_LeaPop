#Libraries 
####################################################################################################################################
import pandas as pd 
import re 
####################################################################################################################################


#All the DDBB 
####################################################################################################################################

#contador_colecciones = pd.read_csv( r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Contador_colecciones.csv')

#######################
ind_col = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_Colecciones_LeaPop.csv')
#######################

#######################
pops = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Pops_LeaPop.csv')
canciones = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Canciones_LeaPop.csv')
promos = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Promos_LeaPop.csv')
miscelaneas = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Miscelanea_LeaPop.csv')
#######################

#######################
individual = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_LeaPop.csv')
colecciones = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Colecciones_LeaPop.csv')
promos_intros = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Promos_Intro_LeaPop.csv')
######################

####################################################################################################################################


#We Define the functions to Update all the DataBases 
####################################################################################################################################


#Updates all the sub-DB that depend on ind_col 
##############################################################################


def easy_updates(ind_col):
    
    #Promos Intros 
    promos_intros = ind_col[((ind_col['Components']==1)& ind_col['Category'].isin(['Promo_App','Promo_Trailer','Promo_Spotify'])) | (ind_col['Category']=='Intro')]
    promos_intros.to_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Promos_Intro_LeaPop.csv', index=False)
    
    #Individuales  
    individual =ind_col[ind_col['Components']==1]
    individual.to_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_LeaPop.csv', index=False)
    
    #Colecciones
    colecciones = ind_col[ind_col['Components']>1]
    colecciones.to_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Colecciones_LeaPop.csv', index=False)
  
##############################################################################

#The Main Update which is The  ind_col DDBB
##############################################################################

def update_ind_col():
    los_dict=[]
    name_pattern = r"(?<=(_EN_|_ES_|_PT_))(.*)(?=(.mp4))"
    dfs = [pops,canciones,promos,miscelaneas]
    los_paths = ind_col['Path'].tolist()
    for df in dfs:
        for k,new_path in enumerate(df['Path']):
            if new_path not in los_paths:
                los_paths.append(new_path)
                #Aux dictionary to save the new entries 
                ######################################################
                aux_dict ={key: None for key in ind_col.columns}
                aux_dict['Path']=df['Path'][k]
                aux_dict['Filename']=df['Nombre_Archivo'][k]
                aux_dict['Components']= df.iloc[k].count()-4 if pd.isna(df['Tag'].iloc[k]) else df.iloc[k].count()-5
                aux_dict['Type']= 'Individual' if  aux_dict['Components'] ==1 else 'Collection'
                aux_dict['Characters']= 'Lea & Pop'
                aux_dict['Tag_IP']= 'IP_LEA' if aux_dict['Characters']== 'Lea & Pop' else  None
                aux_dict['Language'] = 'Español' if '_ES' in df['Nombre_Archivo'][k]  else ('Inglés' if '_EN' in df['Nombre_Archivo'][k] else 'Portugués')
                aux_dict['Category'] = (
                                        'Music' if df is canciones else
                                        'Education' if df is pops else
                                        ('Promo_App' if df['Nombre_Archivo'].str.contains('APP', case=False ).any() else
                                         'Promo_Trailer' if df['Nombre_Archivo'].str.contains('Trailer', case=False).any() else
                                         'Promo_Spotify' if df['Nombre_Archivo'].str.contains('Spotify',case=False).any() else
                                         'Unspecified')
                                        )
                aux_dict['Tag_pieza']= 'VM_POP' if aux_dict['Category']== 'Music' else ( 'SO_POP' if  aux_dict['Category']== 'Education' else None )
                aux_dict['Name'] = re.search(name_pattern, df['Nombre_Archivo'].iloc[k] ).group(0).replace('_', ' ') if re.search(name_pattern, df['Nombre_Archivo'].iloc[k]) else ''
                aux_dict['Activo'] ='Si'
                aux_dict['Season'] =None 
                aux_dict['Number'] =None 
                aux_dict['Version'] =None
                ######################################################
                aux = pd.Series(df.iloc[k])
                aux.drop(['videos_string', 'Path', 'Nombre_Archivo', 'Tag', 'Componentes'],inplace=True)
                aux.dropna(inplace=True)
                # aux = [item.strip() for element in ind_col[ind_col['Filename'].isin(aux.tolist())]['Tag_pieza'].tolist() for item in element.split('|')]
                # aux_dict['Tag_pieza'] = '|'.join(set(aux))
                los_dict.append(aux_dict)
    aux_df =pd.DataFrame(los_dict)
    otra_df = pd.concat([ind_col, aux_df],ignore_index=True)
    otra_df.to_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_Colecciones_LeaPop.csv', index=False)  
    
    easy_updates(otra_df)
##############################################################################


####################################################################################################################################


#Now we actually update all the dataBases 
####################################################################################################################################

update_ind_col() 

####################################################################################################################################