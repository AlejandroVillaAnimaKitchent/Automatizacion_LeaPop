# import os
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
# import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
import io
import base64
from PIL import Image
import ast
import pandas as pd
import sys
sys.path.append("..")
from update_claims_df import update_claims
from webdriver_manager.chrome import ChromeDriverManager
from streamlit_js_eval import streamlit_js_eval
import time
from selenium.webdriver.chrome.service import Service

st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)     


def fight_claim(video_id='a0oZNVhUbrI',tag='CC',contenido=''):
    
    driver.get('https://studio.youtube.com/video/{}/copyright'.format(video_id))
    
    wait = WebDriverWait(driver, 10)  # Adjust the wait time as necessary

    # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="action-button"]'))).click() # Botón de elegir acciones
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="action-button"]')))
    action_buttons = driver.find_elements(By.XPATH, '//*[@id="action-button"]')
    claim_items = driver.find_elements('xpath','//*[@id="asset-title"]')
    claim_items_text = [item.text for item in claim_items] 
    if contenido in claim_items_text:
        index = claim_items_text.index(contenido)
    else:
        index = -1
    # print(contenido)
    # print(index)
    action_buttons[index].click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="text-item-6"]'))).click() # Impugnar
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="agree-checkbox"]'))).click() # Checkbox
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="continue-button"]'))).click() # Continuar
    

    if plantilla[plantilla.Tag==tag].Tipo.values[0] == 'Contenido Original':
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="type-radios"]/tp-yt-paper-radio-button[1]'))).click()
    elif plantilla[plantilla.Tag==tag].Tipo.values[0] == 'Licenciado':
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="type-radios"]/tp-yt-paper-radio-button[2]'))).click()
    else:
        st.error('No estoy listo para ese tipo de reclamación.')
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="continue-button"]'))).click() # Continuar con el tipo elegido
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="continue-button"]'))).click() # Continuar con la disputa (no appeal)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="review-checkbox"]'))).click() # Checkbox
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="continue-button"]'))).click() # Continuar
    
    # 3 checkboxes
    # wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/ytcr-video-flow-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/ytcr-dispute-appeal-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[1]/ytcp-checkbox-lit/div[1]'))).click()
    # wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/ytcr-video-flow-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/ytcr-dispute-appeal-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[2]/ytcp-checkbox-lit/div[1]'))).click()
    # wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/ytcr-video-flow-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/ytcr-dispute-appeal-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[3]/ytcp-checkbox-lit/div[1]'))).click()
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/ytcr-video-flow-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/ytcr-dispute-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[1]/ytcp-checkbox-lit/div[1]'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/ytcr-video-flow-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/ytcr-dispute-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[2]/ytcp-checkbox-lit/div[1]'))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/ytcr-video-flow-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/ytcr-dispute-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[3]/ytcp-checkbox-lit/div[1]'))).click()

    
    # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog"]/div[2]/ytcr-dispute-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[2]/ytcp-checkbox-lit'))).click()
    # wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog"]/div[2]/ytcr-dispute-flow/div/ytcr-dispute-rationale-flow-step/div[1]/div/ytcp-form-checkbox[3]/ytcp-checkbox-lit'))).click()
    
    firma = plantilla[plantilla.Tag==tag].Firma.values[0] # Firma
    text = plantilla[plantilla.Tag==tag].Texto.values[0] # Proof of ownership
    
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="signature"]/div[1]/textarea'))).send_keys(firma)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rationale"]/div[1]/textarea'))).send_keys(text)
        
    driver.find_element('xpath','//*[@id="submit-button"]').click() # Enviar
    

def filter_dispute(value):
    if isinstance(value, str) and (value.startswith('Dispute u') or value.startswith('[Dispute u')):
        return True
    else:
        return False

if __name__ == "__main__":
    st.title('Reclamaciones de Copyright')
    st.markdown('''Aquí encontrarás lo mismo que verías en el CMS si filtraras por "Copyright", pero con la posibilidad de responder a las reclamaciones
                usando plantillas para responder automáticamente. Las reclamaciones de Clan TVE o de vídeos en estado de borrador no aparecen.''', unsafe_allow_html=True)
    
    
    empty_thumb =  b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00\x84\x00\x05\x03\x04\x07\x05\x07\x05\x05\x05\x05\x06\x05\x08\x05\x06\x05\x05\x05\x05\x08\x05\x05\x07\x05\x08\x05\x05\x05\t\x06\x08\t\x05\x05\x13\n\x1c\x0b\x07\x08\x1a\t\x08\x05\x0e!\x18\x1a\x1d\x11\x1f\x13\x1f\x13\x0b"\x18"\x1e\x18\x1c\x12\x13\x12\x01\x05\x05\x05\x07\x06\x07\x05\x08\x08\x05\x12\x08\x05\x08\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\x12\xff\xc0\x00\x11\x08\x00Z\x00x\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1b\x00\x01\x00\x02\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x02\x03\x07\x06\x05\xff\xc4\x00=\x10\x00\x02\x01\x02\x03\x03\x07\x06\r\x05\x00\x00\x00\x00\x00\x00\x00\x02\x01\x03\x04\x05\x11\x12\x06\x13!\x07"12ARa\x14Bqr\x92\xd2\x15U\x81\x84\x91\x94\xb1\xc1\xc2\xc3\xd1\xd3\xf0\x17Qbd\xb3\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xef@\x00\x00\x00\x00\x98\x82t\x81\x882\xd04\x01\x882\xd04\x81\x88&`\x80\x00\x00\x00\x00\x00\x00\x10f\xaab\xa5\x8a*\x01)\x1b\x96\x81\xf26\x83j\xecpVZ7\x1b\xda\xd5\x9a\x15\xda\xde\x8cC:#uf\xb3\xcc\xc2\xa7\x87\x1c\xfc\x0f\x91<\xa8Z\xafW\n\xbaoMku\xfd@\xf6\x1b\x81\xb8<\\\xf2\xa7O\xcd\xc1\xdf\xe5\xbdH\xfc\xb3\x1f\xea\xa2\xfcM?^_\xda\x03\xdbn\x0cZ\x81\xe3W\x95:>v\x0fW\xfc\xb4\xde\xd2\x9f\xcb\x83lr\x9fh\xdd8e\xe2z*\xda\xb7\xdf\x00zw\xa6ie4\xe0\x1bEe\x8dC\xf9#:=(\xd4\xf6\xf5\x15R\xb4\'F\xa5\xe30\xcb\xe8\x92\xdde\x02\xb8\x0c\x00\x00\x00\x00\x00\xc9\x0b\xb6\x8b\xaaT\xa4\x85\xfb9\xe2\xa0p\xacz\xe2n/1\x0b\x86mSV\xee\xe5\xb5t\xf3V\xb3"\xfc\x9aU \xa6MI\xe7;w\x9e\xa3{O%\xbc\x12\xc2q\x0b\xab[$x\xa57UV\x96\xb6\xe2\xab\xab\xa6t\xf6\xf0\x86\x02\x98=6\xdel\xac`Si)u7\tu\xbd^z*UW\xa3\xa6[\x9b\x13\x94\xaeL\xa5\xcb\xad\x86\xdda?\x0cyn\xaa\x8bmN\xf5\xad\xf7K\xb9\xdd:\xc4\xe9Z\xb9\xe7\xaf&_\x0c\xc0\xf1\xa0\xf5{\x0b\xb2\x11\x8e\xa5\xd5j\xb7sj\xb4j-\x15T\xa4\xae\xedU\x93^m\xc62\\\xa5O7\x88\xdbM\xa5{\x8bV\x98v\xb5\xabV\xdd\x9dz\xac\xd4\x9eRe|8\x01\xf5\xb9?\xaf4qL5\xb5i\x8a\xb5Z\xdd\xfcV\xb22e\xf4\xca\x9d\x82\xe6\x0e\'\xb2\xed\xa7\x10\xc3%zV\xf2\xd3\xfe\xcav\xeb\xbf8\n.A.@\x00\x00\x00\x00\x12\x85\xdbF\xe3\x1e\x92\x8c\x1b\xe9>\x908]\xcaJU\xac\x8d\xd2\x95j\xa3z\xd1Vb~\xc3\x1ao)*\xe8\xd2\x8c\x92\xb2\x8e\xad\x94\xab/\x18\x95n\xc9\xcc\xfb{m\x84\xd4\xb1\xbb\xbavI\xdc\xddU\xa9qoZ\x17\x99+U\xe5\xe5Z{\x1a&Z\x0f\x85\xaa;\xd0\x05\xacB\xfe\xe2\xf5\x96\xad\xed\xd5k\xa7X\xd0\x8fR\xab;*t\xe4\xbf\xda\t|J\xe5\xa8-\x94\xdd\xd7ku\x9dKk5_s\x1a[8\xe6te\x9f\x12\xa6d\x81k\x0f\xc4\xael\xb5\xf9%\xdd{]\xeci\xab\xbb\xaa\xc9\xa9{5}%Y\x9f\xe4\xf1in\xd9f\xed\x923\x1a\xa3\xbd\x00}M\x92Mx\x8e\x18\xbf\xee[7\xb2\xf0\xf3\xf6\x1d\xa6\xe1\x8e]\xc9\xae\x15R\xb5\xdd+\xe6IZ6\x9b\xc7\xde\xca\xe4\xafZRQ\x12\x97zcVs\x97\xdet\xba\x8c\x06\xa6 H\x00\x00\x00\x00\x00J\xc9\x00\r\x9a\xb5sYa\xa3\xbb*\xb3\x1e\xc9\xad\xad\xad\xdf\xafko>\xb5\xbd\x19\xfc f\x06\xa6\xc3,[\xad\x87\xd9\xb7\xcdh\xfb\xa6?\x04X|Yg\xf5j?\xa1\xbf1\x98\x1a\xd7\x0c\xb2^\xae\x1ff\xbf4\xa3\xee\x9bV\xde\x82u-m\xd3\xd5\xb7\xa2\xbf\x84\x8c\xc6`l\x97\xec\xec^\xaa\xc7\x05\x8fU{\x0c&H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xd9'
    
    # plantilla = pd.read_excel(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\Plantillas_Reclamaciones_Copyright.xlsx')
    plantilla = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\Copyright\Plantillas_Reclamaciones_Copyright.xlsx')
    # claim_excel = pd.read_excel(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\Copyright_Claims.xlsx')
    claim_excel = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\Copyright\Copyright_Claims.xlsx')
    
    def clan(s):
        return 'clan tve' in str.lower(s)
    
    def evaluate_string(s):
        try:
            return ast.literal_eval(s)
        except (ValueError, SyntaxError):
            return s
    
    claim_excel = claim_excel[~claim_excel['title'].str.contains('clan tve', case=False, na=False)].reset_index(drop='True')
    claim_excel['status'] = claim_excel['status'].apply(evaluate_string)
    claim_excel['claimer'] = claim_excel['claimer'].apply(evaluate_string)
    claim_excel['claimed_content'] = claim_excel['claimed_content'].apply(evaluate_string)
    
    claim_excel_ = claim_excel.explode('status').reset_index(drop='True')
    
    
    
    st.info('Si quieres consultar, modificar o añadir alguna plantilla de respuesta, las tienes en el siguiente archivo: '+ \
            r'\\'+r'\\cancer\Material_Definitivo\telerin\Copyright\Plantillas_Reclamaciones_Copyright.xlsx', icon="ℹ️")
    
    update = st.button('Actualizar las reclamaciones',key='update')    
    tabs = st.tabs(['Pendientes','En Proceso','Rechazadas (último mes)','Perdidas (último mes)'])
    column_names = ['Miniatura','ID + Título','Reclamador','Contenido Reclamado','Plantilla','Fecha Actualización']
    column_names2 = ['Miniatura','ID + Título','Reclamador','Contenido Reclamado','Status','Fecha Actualización']
    
    claim_dict = {}
    content_dict = {}
    
    
    
    # Get the current date
    current_date = pd.Timestamp.now()
    
    # Calculate the first day of the previous month
    first_day_of_previous_month = pd.Timestamp(current_date.year, current_date.month - 1, 1) if current_date.month != 1 else pd.Timestamp(current_date.year - 1, 12, 1)
            
    
    # Pending
    with tabs[0]:
        final = st.button('Responder a todas las reclamaciones señaladas', key='final')
    
            
        with st.expander("Desplegar"):
            
            # pending = claim_excel[~((claim_excel.status.apply(filter_dispute)) | (claim_excel.status == 'Lost'))].reset_index(drop='True')
            pending = claim_excel[claim_excel.status.str.startswith('P') | claim_excel.status.str.startswith("['P")].reset_index(drop='True')
            # pending = claim_excel[claim_excel.status.str.startswith('P')].reset_index(drop='True')
            
            if len(pending)==0:
                st.balloons()
                st.text('¡Felicidades, estás al día con las reclamaciones! (Al menos que no esté actualizado.)')
            

            columns = st.columns([1,3,3,2,2,2], gap='small')
            for i in range(len(columns)):
                with columns[i]:
                    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(column_names[i]), unsafe_allow_html=True)
            
            for i in range(len(pending)):
                
                # columns = st.columns([1,3,3,2,2,2], gap='small')
                
                idd = pending.loc[i].videoid
                title = pending.loc[i].title
                claimer = pending.loc[i].claimer
                claimed_content = pending.loc[i].claimed_content
                thumb = pending.loc[i].thumb64
                items = pending.loc[i].claimer.split("',")
                date = pending.loc[i].fecha
                
                for j in range(len(items)):
                    
                    columns = st.columns([1,3,3,2,2,2], gap='small')
                    with columns[0]:
                        
                        image_bytes = base64.b64decode(thumb)
                        image_io = io.BytesIO(image_bytes)
                        image = Image.open(image_io)
                        
                        if image.height<68:
                            image_io = io.BytesIO(empty_thumb)
                            image = Image.open(image_io)
                            image.thumbnail((68, 120))
                        
                        st.image(image, use_column_width=True)
     
                    with columns[1]:
                        st.write(idd+' :\n'+title)
                        
                    with columns[2]:
                        items = pending.loc[i].claimer.split("',")
                        item = items[j]
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
                            
                    with columns[3]:
                        try:
                            items = ast.literal_eval(pending.loc[i].claimed_content)
                            item = items[j]
                        except:
                            item = str(pending.loc[i].claimed_content)
                        
                        
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
                                
        
                    with columns[4]:
                        items = pending.loc[i].claimer.split("',")
                        item = items[j]
                        selections = tuple(['']+list(plantilla.Tag))
                        selectbox = st.selectbox('Elige una plantilla para responder',selections,key=idd+str(j))
                        claim_dict[idd+str(j)] = selectbox
                        try:
                            items = ast.literal_eval(pending.loc[i].claimed_content)
                            item = items[j]
                        except:
                            item = str(pending.loc[i].claimed_content)
                        content_dict[idd+str(j)] = item
                    
                    with columns[5]:
                        date_str = pending.loc[i].fecha.strftime('%Y-%m-%d %H:%M:%S')
                        st.markdown(f'<div style="text-align: center;">{date_str}</div>', unsafe_allow_html=True)
    
    
    # Under review
            
    with tabs[1]:
        with st.expander("Desplegar"):
            dispute = claim_excel[claim_excel.status.apply(filter_dispute)].reset_index(drop='True')
            
            columns = st.columns([1,3,3,2,2,2], gap='small')
            for i in range(len(columns)):
                with columns[i]:
                    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(column_names2[i]), unsafe_allow_html=True)
        
                
            for i in range(len(dispute)):
                
                idd = dispute.loc[i].videoid
                title = dispute.loc[i].title
                claimer = dispute.loc[i].claimer
                claimed_content = dispute.loc[i].claimed_content
                thumb = dispute.loc[i].thumb64
                
                items = dispute.loc[i].claimer.split("',")
                    
                for j in range(len(items)):
                        
                    columns = st.columns([1,3,3,2,2,2], gap='small')
                    with columns[0]:
                        
                        image_bytes = base64.b64decode(thumb)
                        image_io = io.BytesIO(image_bytes)
                        image = Image.open(image_io)
                        
                        if image.height<68:
                            image_io = io.BytesIO(empty_thumb)
                            image = Image.open(image_io)
                            image.thumbnail((68, 120))
                                                
                        st.image(image, use_column_width=True)
                        
                    with columns[1]:
                        st.write(idd+' :\n'+title)
                                
                    with columns[2]:
                        items = dispute.loc[i].claimer.split("',")
                        item = items[j]
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
        
                    with columns[3]:
                        try:
                            items = ast.literal_eval(dispute.loc[i].claimed_content)
                            item = items[j]
                        except:
                            item = str(dispute.loc[i].claimed_content)
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
            
                    with columns[4]:
    #                     st.write(j)
    #                     st.write(items)
                        items = dispute.loc[i].status.split("', ")
                        item = items[j]
                        st.write(item.replace("'",'').replace(']','').replace('[','').replace('\n','. ').replace('\\n','. ')+'.')
                        
                    with columns[5]:
                        date_str = dispute.loc[i].fecha.strftime('%Y-%m-%d %H:%M:%S')
                        st.markdown(f'<div style="text-align: center;">{date_str}</div>', unsafe_allow_html=True)
    
    
        
    # Rejected
    with tabs[2]:
        with st.expander("Desplegar"):
            
            rejected = claim_excel[
                    (claim_excel.status.str.startswith('Dispute re') | claim_excel.status.str.startswith("['Dispute re")) &
                    (claim_excel.fecha >= first_day_of_previous_month)
                ].reset_index(drop=True)
            
            columns = st.columns([1,3,3,2,2,2], gap='small')
            for i in range(len(columns)):
                with columns[i]:
                    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(column_names2[i]), unsafe_allow_html=True)
            
                
            for i in range(len(rejected)):
                
                columns = st.columns([1,3,3,2,2,2], gap='small')
                
                idd = rejected.loc[i].videoid
                title = rejected.loc[i].title
                claimer = rejected.loc[i].claimer
                claimed_content = rejected.loc[i].claimed_content
                thumb = rejected.loc[i].thumb64
                items = rejected.loc[i].claimer.split("',")
                    
                for j in range(len(items)):
                    
                    columns = st.columns([1,3,3,2,2,2], gap='small')
                        
                    with columns[0]:
                        
                        image_bytes = base64.b64decode(thumb)
                        image_io = io.BytesIO(image_bytes)
                        image = Image.open(image_io)
                        
                        if image.height<68:
                            image_io = io.BytesIO(empty_thumb)
                            image = Image.open(image_io)
                            image.thumbnail((68, 120))
                        
                        st.image(image, use_column_width=True)
                        
                    with columns[1]:
                        st.write(idd+' :\n'+title)
                        
                    with columns[2]:
                        items = rejected.loc[i].claimer.split("',")
                        item = items[j]
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
                            
                    with columns[3]:
                        try:
                            items = ast.literal_eval(rejected.loc[i].claimed_content)
                            item = items[j]
                        except:
                            item = str(rejected.loc[i].claimed_content)
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
            
                    with columns[4]:
                        try:
                            items = ast.literal_eval(rejected.loc[i].status)
                            item = items[j]
                        except:
                            item = str(rejected.loc[i].status)
                            
                        stat = (item.replace("'",'').replace("']",'').replace("['",'').replace('\n','. ').replace('\\n','. '))    
                        st.markdown(f'<div style="text-align: center;">{stat}</div>', unsafe_allow_html=True)
        
                    with columns[5]:
                        date_str = rejected.loc[i].fecha.strftime('%Y-%m-%d %H:%M:%S')
                        st.markdown(f'<div style="text-align: center;">{date_str}</div>', unsafe_allow_html=True)
                        
    # Lost
    with tabs[3]:
        with st.expander("Desplegar"):
        
            # lost = claim_excel[claim_excel.status.str.startswith('L') | claim_excel.status.str.startswith("['L")].reset_index(drop='True')

            lost = claim_excel[
                (claim_excel.status.str.startswith('L') | claim_excel.status.str.startswith("['L")) &
                (claim_excel.fecha >= first_day_of_previous_month)
                ].reset_index(drop=True)
            
            columns = st.columns([1,3,3,2,2,2], gap='small')
            for i in range(len(columns)):
                with columns[i]:
                    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(column_names2[i]), unsafe_allow_html=True)
            
            
            for i in range(len(lost)):
                
                columns = st.columns([1,3,3,2,2,2], gap='small')
                
                idd = lost.loc[i].videoid
                title = lost.loc[i].title
                claimer = lost.loc[i].claimer
                claimed_content = lost.loc[i].claimed_content
                thumb = lost.loc[i].thumb64
                items = lost.loc[i].claimer.split("',")
                
                for j in range(len(items)):
                    
                    columns = st.columns([1,3,3,2,2,2], gap='small')
                    
                    with columns[0]:
                        
                        image_bytes = base64.b64decode(thumb)
                        image_io = io.BytesIO(image_bytes)
                        image = Image.open(image_io)
                        
                        if image.height<68:
                            image_io = io.BytesIO(empty_thumb)
                            image = Image.open(image_io)
                            image.thumbnail((68, 120))
                        
                        st.image(image, use_column_width=True)
                        
                    with columns[1]:
                        st.write(idd+' :\n'+title)
                        
                    with columns[2]:
                        items = lost.loc[i].claimer.split("',")
                        item = items[j]
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
                        
                    with columns[3]:
                        try:
                            items = ast.literal_eval(lost.loc[i].claimed_content)
                            item = items[j]
                        except:
                            item = str(lost.loc[i].claimed_content)
                        st.write(item.replace("'",'').replace(']','').replace('[',''))
                            
                    with columns[4]:
                        try:
                            items = ast.literal_eval(lost.loc[i].status)
                            item = items[j]
                        except:
                            item = str(lost.loc[i].status)
                            
                        stat = (item.replace("'",'').replace("']",'').replace("['",'').replace('\n','. ').replace('\\n','. '))    
                        st.markdown(f'<div style="text-align: center;">{stat}</div>', unsafe_allow_html=True)
                        
                    with columns[5]:
                        date_str = lost.loc[i].fecha.strftime('%Y-%m-%d %H:%M:%S')
                        st.markdown(f'<div style="text-align: center;">{date_str}</div>', unsafe_allow_html=True)
            
    
        
    
    if update:
        
        st.info('Actualizando lista. Esto puede tardar unos minutos.') 
        update_claims()
        time.sleep(1)
        st.info('Lista actualizada, actualizando página.')
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        
        
        
        
        
    if final:
        
        # options = Options()
        # # options.add_argument("--headless=new")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-features=NetworkService")
        # options.add_argument("--window-size=1920x1080")
        # options.add_argument("--disable-features=VizDisplayCompositor")
        # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.5845.110')
        
        # # driver = webdriver.Chrome(options=options) 
        # driver = webdriver.Chrome(options=options, service=ChromeDriverManager().install())
        
        
        
        service_ = Service(r'C:\Users\pablo.perezmartin\.wdm\drivers\chromedriver\win64\116.0.5845.97\chromedriver-win32\chromedriver.exe')
        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=NetworkService")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.5845.110')
        
        # driver = webdriver.Chrome(options=options) 
        driver = webdriver.Chrome(options=options, service=service_)
        # driver = webdriver.Chrome(options=options, service=ChromeDriverManager().install())
        
        driver.get('https://www.youtube.com/')
        # cookies = pickle.load(open(r"C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\pkls\cookies_cyber.pkl", "rb"))
        try:
            cookies = pickle.load(open(r"C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\pkls\cookies_cyber.pkl", "rb"))
        except:
            try:
                cookies = pickle.load(open(r"C:\Users\alejandro.villa\Documents\Codigos\Automatizacion\pkls\cookies_cyber.pkl", "rb"))
            except:
                raise Exception("No se eonctraron cookies disponibles.")
        
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('https://www.youtube.com/')
        
        claim_values = list(plantilla.Tag)
        st.info('Procesando reclamaciones. Esto puede tardar unos minutos.')
        failed = []
        for key in [k for (k,v) in claim_dict.items() if v in claim_values]:
            try:
                fight_claim(key[:-1],claim_dict[key],content_dict[key])
                time.sleep(3.5)
            except:
                failed.append((key[:-1],content_dict[key]))
        if len(failed)>0:
            st.error('Han fallado {} reclamacione(s).'.format(len(failed)))
        for elem in failed:
            st.info('El video {} con reclamación {} ha fallado. Probablemente estaba mal clasificado y se arregle al actualizar la lista de nuevo.'.format(elem[0],elem[1]))    
        update_claims()
        time.sleep(1)
        st.info('Lista actualizada, actualizando página.')
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
            
            
            