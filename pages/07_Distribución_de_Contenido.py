import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyexcel_ods import get_data
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable


hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     


JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""
#Functions definition 
#######################################################################################################################################


######################################################
def drag_and_drop_file(drop_target, path):
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)
######################################################

######################################################
def upload_file(driver, file_path):
    drop_area = driver.find_element('xpath','//*[@id="immersive-container"]/div[1]/div/div')  
    drag_and_drop_file(drop_area, file_path)
######################################################
    
######################################################
def update_progress(progress_dict, progress_text):
    lines = progress_text.split('\n')
    for i in range(0, len(lines), 2):
        filename = lines[i]
        progress_dict[filename] = lines[i+1]
    return progress_dict
######################################################

######################################################
def get_file_path(file):

    #Ind_Col_Lea =  pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_LeaPop.csv')
    pops = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Pops_LeaPop.csv')
    canciones = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Canciones_LeaPop.csv')
    promos = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Promos_LeaPop.csv')
    miscelaneas = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Cols_DB\Miscelanea_LeaPop.csv')
    individual = pd.read_csv(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Lea&Pop Databases\Individuales_LeaPop.csv')
    
    
    # Match a las miniaturas
    if file.endswith('.png'):
        file_path = os.path.join(r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Thumbs',file)
        return file_path
    
    # Match a los vídeos
    else:
        individual_match = individual[individual['Filename'] == file]
        if not individual_match.empty:
            return individual_match['Path'].values[0]
        
        pops_match = pops[pops['Nombre_Archivo'] == file]
        if not pops_match.empty:
            return pops_match['Path'].values[0]
        
        canciones_match = canciones[canciones['Nombre_Archivo'] == file]
        if not canciones_match.empty:
            return canciones_match['Path'].values[0]
        
        promos_match = promos[promos['Nombre_Archivo'] == file]
        if not promos_match.empty:
            return promos_match['Path'].values[0]
        
        miscelaneas_match = miscelaneas[miscelaneas['Nombre_Archivo'] == file]
        if not miscelaneas_match.empty:
            return miscelaneas_match['Path'].values[0]
######################################################

 
######################################################
def find_file(filename):
    # Check in specific folders first
    specific_folders = [
        r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Thumbs',
        r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Episodios sueltos',
        r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Canciones sueltas',
        r'\\cancer\Material_Definitivo\LEA\COLECCIONES\Colecciones'
        ]
    for folder in specific_folders:
        for file in os.listdir(folder):
            if file == filename:
                return os.path.join(folder, filename)
    
    # If not found in the main folders search in the docs.
    get_file_path(filename)
    
    # If not found in specific folders and file trackers, walk the root directory
    root_dirs = [
        ]
    for root_dir in root_dirs:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if filename in filenames:
                return os.path.join(dirpath, filename)
            
    st.error('No se pudo encontrar el arhivo ' + file)

    return None
######################################################

######################################################
def run_selenium(file):
    name = str()
    distrib_df = pd.read_excel(file)
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.6099.130')
    
    svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(options=options, service=svc)
    
    driver.get('https://www.youtube.com/')

    
    try:
        cookies = pickle.load(open(r"C:\Users\pablo.perezmartin\Documents\cleoycuquin\Cookies\pkls\cookies_pablo.pkl", "rb"))
    except:
        try:
            cookies = pickle.load(open(r"C:\Users\alejandro.villa\Documents\Codigos\Automatizacion\pkls\cookies_cyber.pkl", "rb"))
        except:
            raise Exception("No se encontraron cookies disponibles.")
            
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get('https://www.youtube.com/')

    try: 
        driver.get('https://studio.youtube.com/owner/iHywrp4i6tV0ZP3a3-_GZA/delivery/packages?o=iHywrp4i6tV0ZP3a3-_GZA')
        
        driver.find_element('xpath','//*[@id="validate-upload-button"]').click() # Validar y Subir
        upload_file(driver,os.path.join(r'A:\Automatizacion_LEA\temp',final_filename)) # Subir el excel
        time.sleep(5)
        progress = {}
        progress_list = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="progress-list"]')))
        progress_text = progress_list.text
        s = progress_text
        lines = s.split('\n')
    except: raise Exception('Los cookies no se cargaron correctamente, comuníquese con su programador de confianza.')
        
    
    for i in range(0, len(lines), 2):
        filename = lines[i]
        progress[filename] = lines[i+1]
        
    
    while len(set(list(progress.values())))>1:
        file_errors = [k for k, v in progress.items() if v != '100% uploaded']
        if len(file_errors)>0:
            info.info('Se ha producido un error con el archivo de metadata. Reintentando.')
            try:
                upload_file(driver,os.path.join(r'A:\Automatizacion_LEA\temp',final_filename))
            except:
                upload_file(driver,os.path.join(r'A:\Automatizacion_LEA\temp',final_filename))
            time.sleep(2)
            progress_list = driver.find_element('xpath','//*[@id="progress-list"]')
            progress_text = progress_list.text
            progress = update_progress(progress, progress_text)    
         
    
    bar_num = 0.0
    
    minis = set(distrib_df.custom_thumbnail.values)
    num_minis = len(minis)
    upload_bar = st.progress(bar_num, 'Subiendo miniaturas.')
    for mini in minis:
        print(mini)
        mini_path = find_file(mini)
        # print()
        upload_file(driver, mini_path)
        time.sleep(1)
        bar_num += 1/num_minis
        upload_bar.progress(min(bar_num,0.99), 'Subiendo miniaturas.')
    
    upload_bar.progress(1.0, 'Miniaturas subidas.')

    
    # Subir vídeos 
    videos = set(distrib_df.filename.values)
    num_videos = len(videos)
    bar_num = 0.0
    # upload_bar.progress(bar_num, 'Subiendo vídeos.')
    
    for video in videos:
        print(video)
        video_path = find_file(video)
        # print(video_path)
        upload_file(driver, video_path)
        time.sleep(1)
        bar_num += num_videos
        upload_bar.progress(min(bar_num,0.99), 'Subiendo vídeos.')
    
    progreso_archivos = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expand-button"]')))
    while progreso_archivos.text not in ['Uploads complete', 'Subidas completadas']:
        progreso_archivos = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expand-button"]')))
        pass
    
    upload_bar.progress(1.0, 'Vídeos y miniaturas subidos, comprobando si hay errores.')
    
    # Comprobación final de que se han subido todos bien.
    errors = 0
    progress = {}
    progress_list = driver.find_element('xpath','//*[@id="progress-list"]')
    progress_text = progress_list.text
    s = progress_text
    lines = s.split('\n')
    progress = {}
    fail = False
    for i in range(0, len(lines), 2):
        filename = lines[i]
        progress[filename] = lines[i+1]
    
    while len(set(list(progress.values())))>1:
        file_errors = [k for k, v in progress.items() if v != '100% uploaded']
        info.info('Se han encontrado errores con {} archivo(s). Reintentando.'.format(len(file_errors)))
        for file in file_errors:
            file_path = find_file(file)
            upload_file(driver, file_path)
      
         
        errors+=1
        if errors>10:
            file_string = '\n'.join(file_errors)
            st.error('Los siguientes archivos parecen dar errores, por favor revísalos antes de interntarlo de nuevo: \n'+file_string)
            fail = True
            break
        
        # time.sleep(60)
        progreso_archivos = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expand-button"]')))
        while progreso_archivos.text != 'Uploads complete':
            progreso_archivos = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="expand-button"]')))
            pass
        time.sleep(5)
        
        progress_list = driver.find_element('xpath','//*[@id="progress-list"]')
        progress_text = progress_list.text
        progress = update_progress(progress, progress_text)  
        
    if not fail:
        
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable(By.XPATH,'//*[@id="process-package-button"]')).click() # Procesar paquete
        st.balloons()
        info.info("""
                Se han subido todos los archivos correctamente y se va a publicar el contenido. 
                Espera brevemente y comprueba en el canal apropiado.
                """)
                
    driver.quit()
    upload_bar.empty()
             
    return name
######################################################

#######################################################################################################################################

#Deployment 
#######################################################################################################################################

if __name__ == "__main__":
    st.title('Distribución de Contenido')
    st.markdown('''Aquí podrás subir el excel de distribución y yo me encargo de buscar todo tu contenido dentro de Material Definitivo (Madrid).
                Si no tienes el contenido en Material Definitivo - telerin, utiliza el Content Delivery de YouTube, por favor...
        ''', unsafe_allow_html=True)
    
    file = st.file_uploader("Suba el Archivo Excel de su contenido:", type=["xlsx",'xls','ods'])  
    retry = st.button('Reintentar')
    if file or retry:
    
        correct_file = True
        file_details = {"FileName":file.name,"FileType":file.type,"FileSize":file.size}
        
        if file_details["FileType"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            final_filename = file.name.replace('.xlsx','_temp.xlsx')
            # with open(os.path.join(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\temp',final_filename), "wb") as f:
            #     f.write(file.getbuffer())
            df = pd.read_excel(file)
            # df.to_excel(os.path.join(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\temp',final_filename), index=False)
            df.to_excel(os.path.join(r'A:\Automatizacion_LEA\temp',final_filename), index=False)
                
        elif file_details["FileType"] == "application/vnd.ms-excel":
            st.write('Convirtiendo el archivo .xls a .xlsx')
            df = pd.read_excel(file)
            final_filename = file.name.replace('.xls','_temp.xlsx')
            # df.to_excel(os.path.join(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\temp',final_filename), index=False)
            df.to_excel(os.path.join(r'A:\Automatizacion_LEA\temp',final_filename), index=False)
            
        elif file_details["FileType"] == "text/csv":
            st.write('Convirtiendo el archivo .csv a .xlsx')
            df = pd.read_csv(file)
            final_filename = file.name.replace('.csv','_temp.xlsx')
            # df.to_excel(os.path.join(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\temp',final_filename), index=False)
            df.to_excel(os.path.join(r'A:\Automatizacion_LEA\temp',final_filename), index=False)
                
        elif file_details["FileType"] == "application/vnd.oasis.opendocument.spreadsheet":
            st.write('Convirtiendo primera hoja del archivo .ods a .xlsx')
            data = get_data(file)
            sheet_name, sheet_data = data.items()[0]
            df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])
            final_filename = file.name.replace('.ods','_temp.xlsx')
            # df.to_excel(os.path.join(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\temp',final_filename), index=False)         
            df.to_excel(os.path.join(r'A:\Automatizacion_LEA\temp',final_filename), index=False)         
        
        else:
            correct_file = False
            
            
        if correct_file:    
            info = st.info('Archivo recibido. Se va a intentar publicar el contenido, no cierres la página hasta que acabe.')
            run_selenium(file)
            # os.remove(os.path.join(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\temp',final_filename))
            os.remove(os.path.join(r'A:\Automatizacion_LEA\temp',final_filename))
        else:
            st.error('Formato de archivo no soportado. Inténtalo con un excel/ods/csv.')
            
#######################################################################################################################################
