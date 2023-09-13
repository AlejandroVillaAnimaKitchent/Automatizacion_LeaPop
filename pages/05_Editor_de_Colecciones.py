import streamlit as st
import pandas as pd

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)    

def is_duplicate(element, df):
    element= [value for value in element if pd.notna(value)]
    reality = False
    element_str = element[1]
    for i in element[2:]:
        element_str = element_str + ',' + str(i)
    if element_str in df['videos_string'].values:
        reality = True
        duplicate_path = df.loc[df['videos_string'] == element_str, 'Path'].values[0]
        return reality, element_str, duplicate_path
    else: 
        return reality, element_str

def process_collection_file(df2):
    df2= df2.transpose()

    for index in range(len(df2)):
        line = df2.loc[index].tolist()
        if is_duplicate(line, df)[0]:
            st.error(f"La coleccción {line[0]} ya se encuentra en la base de datos.")
            st.error(f"Su ubicación es {is_duplicate(line, df)[2]}")
            df2.drop(index, inplace=True)
    df2 = df2.transpose()
    return df2

def handle_choice(choice):
    global file_path
    global df
    if choice =="Ninguna":
         st.error('Debe Escoger una Opción válida')   
    elif choice == "Cuquines":
        file_path = r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Cuquines_DB.xls'
        df = pd.read_excel(file_path)
    elif choice == "Canciones":
        file_path = r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Canciones_DB.xls'
        df = pd.read_excel(file_path)
    elif choice == "Promos":
        file_path = r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Promos_DB.xls'
        df = pd.read_excel(file_path)
    elif choice == "Miscelaneas":
        file_path = r'\\cancer\Material_Definitivo\telerin\COLECCIONES\Colecciones_DataBase\Miscelaneas_DB.xls'
        df = pd.read_excel(file_path)

# Streamlit app
def main():
    st.title("Editor de Colecciones")

    # Create a label and dropdown menu for the user to choose their video collection
    st.subheader("Escoge el tipo de Colección que desea hacer")
    st.write('Esta página editará el archivo de colecciones que desea hacer contrastándolo con nuestras bases de datos y eliminando aquellas colecciones que ya han sido realizadas.')
    choices = ["Ninguna","Cuquines", "Canciones", "Promos", "Miscelaneas"]
    choice = st.selectbox("Seleccione un tipo de colección", choices)
    file = st.file_uploader("Suba el Archivo Excel de sus colecciones", type=["xlsx", "xls","ods"])
    # Create a button to submit the choice
    
    if file is not None and choice:
        handle_choice(choice)
        try: 
            df2 = pd.read_excel(file,header=None)
            st.success("Archivo procesado exitosamente. Las colecciones que ha ingresado son:")
            st.dataframe(df2) 
        except:  #Exception as e:
            #st.error(f"Error: {str(e)}")
            st.error('Debe subir un archivo y escoger una colección válida')
            
        if st.button("Enviar"):
            df2= process_collection_file(df2)
            try:
                df2.to_excel(f'\\\\cancer\\Material_Definitivo\\telerin\\COLECCIONES\\{file.name}',index=False, header=False)
                st.success("De las colecciones entregadas se tuvieron en cuenta las siguientes:")
                st.dataframe(df2)
                st.success(f'Su nuevo archivo {file.name}  está en la carpeta \\\\cancer\\Material_Definitivo\\telerin\\COLECCIONES')
                st.success('Puede dirigirse directamente a la aplicación a hacer sus colecciones.')
            except PermissionError: 
                st.error('El archivo que se intenta reescribir está abierto, por favor cierrelo.')
    else: 
        st.success('Debe subir un archivo y escoger una colección válida')

if __name__ == "__main__":
    main()


