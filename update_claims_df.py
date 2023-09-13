from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import datetime as dt
from selenium.webdriver.chrome.service import Service


def update_claims():
    # df = pd.read_excel(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\Copyright_Claims.xlsx')
    # df = pd.read_excel(r'A:\Automatizacion\Copyright_Claims.xlsx')
    df = pd.read_excel(r'\\cancer\Material_Definitivo\telerin\Copyright\Copyright_Claims.xlsx')
    df = pd.DataFrame(columns=['videoid', 'title', 'status', 'thumb64', 'claimer', 'claimed_content','fecha'])
    
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
    
    
    ##### Get Claims (this is only the first page)
    # driver.get('https://studio.youtube.com/owner/iHywrp4i6tV0ZP3a3-_GZA/videos/upload?o=iHywrp4i6tV0ZP3a3-_GZA&filter=%5B%7B%22name%22%3A%22HAS_COPYRIGHT_CLAIM%22%2C%22value%22%3A%22VIDEO_HAS_COPYRIGHT_CLAIM%22%7D%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D')
    
    driver.get('https://studio.youtube.com/owner/iHywrp4i6tV0ZP3a3-_GZA/videos/upload?o=iHywrp4i6tV0ZP3a3-_GZA&filter=%5B%7B%22name%22%3A%22HAS_COPYRIGHT_CLAIM%22%2C%22value%22%3A%22VIDEO_HAS_COPYRIGHT_CLAIM%22%7D%2C%7B%22name%22%3A%22VISIBILITY%22%2C%22value%22%3A%5B%22HAS_SCHEDULE%22%2C%22SPONSORS_ONLY%22%2C%22UNLISTED%22%2C%22PRIVATE%22%2C%22PUBLIC%22%5D%7D%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D')
    
    
    wait = WebDriverWait(driver, 30)  # Set the wait time to 20 seconds
    title_containers = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="video-title"]')))
    
    
    list_of_ids = [title_containers[i].get_attribute('href').split('video/')[1][:11] for i in range(len(title_containers))]
    list_of_titles = [title_containers[i].text for i in range(len(title_containers))]
    # image_containers =  wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="img-with-fallback"]')))
    image_containers =  wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="video-thumbnail-container"]/ytcp-thumbnail/div/ytcp-img-with-fallback/div')))
    list_of_thumbs = [img.screenshot_as_base64 for img in image_containers]
    
    ##### Get Claims from pages 2 to pages_to_scroll
    pages_to_scroll = 2
    for i in range(pages_to_scroll-1):
        driver.find_element('xpath','//*[@id="navigate-after"]').click()
        wait = WebDriverWait(driver, 30)  # Set the wait time to 20 seconds
        title_containers = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="video-title"]')))
        list_of_ids += [title_containers[i].get_attribute('href').split('video/')[1][:11] for i in range(len(title_containers))]
        list_of_titles += [title_containers[i].text for i in range(len(title_containers))]
        # image_containers =  wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="img-with-fallback"]')))
        image_containers =  wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="video-thumbnail-container"]/ytcp-thumbnail/div/ytcp-img-with-fallback/div')))
        list_of_thumbs += [img.screenshot_as_base64 for img in image_containers]
    
    
    ##### Get claim data (status, claimer and content claimed)
    list_of_claimers = []
    list_of_status = []
    list_of_content = []
    
    passed_ids = []
    weird_ids = []
    # a_ids = ['k5oGCYeMZQs','KXoQkSZtDfU','cbIkrnpQJhI','Go_P1fE9Glw','Lyy-xxwuClU']
    # a_ids = ['k5oGCYeMZQs','KXoQkSZtDfU']
    
    
    for videoid in list_of_ids:
    # for videoid in a_ids:
        
    # for videoid in list_of_ids[list_of_ids.index(videoid)+1]:
        # videoid = 'k5oGCYeMZQs'
        # videoid = 'KXoQkSZtDfU'
        # videoid = 'EhUK1QceGVo'
        driver.get('https://studio.youtube.com/video/{}/copyright'.format(videoid))
        
        #Claimer
        try:
            triggers = WebDriverWait(driver, 60).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="impact-text-container"]')))
            multi = len(triggers)>1
            if multi:
                
                for i in range(2):
                    claimers = []
                    claims = []
                    statuses = []
                    
                    three_dots = driver.find_elements('xpath','//*[@id="action-button"]') # Find 3 dots
                    solutions = driver.find_elements('xpath','//*[@id="dispute-status"]') # Statuses of active ones
                    for j in range(len(triggers)):
                    # for j in range(len(triggers)-1,-1,-1):
                        # Claimers
                        # j=0
                        trigger = triggers[j]
                        ActionChains(driver).move_to_element(trigger).perform()
                        # targets = WebDriverWait(driver, 30).until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="slot-wrapper"]/ytcp-paper-tooltip-body/div/div[2]')))
                        
                        try:
                            targets = WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="slot-wrapper"]/ytcp-paper-tooltip-body/div[2]')))
                        except:     
                            targets = WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.XPATH, '//*[@id="slot-wrapper"]/ytcp-paper-tooltip-body/div/div[2]')))
                        
                        claimers.append(targets[0].text)
                        
                        # Claimed items
                        claim_item = driver.find_element('xpath','//*[@id="main"]/div/ytcp-animatable[19]/ytcr-video-home-page/ytcr-video-home-section/ytcr-video-content-list/div[{}]/ytcr-video-content-list-claim-row/div[1]/div[2]/div[1]'.format(j+2))
                        claims.append(claim_item.text)
                   
             
                        # Statuses
                        # j=0
                        elem = three_dots[j]
                        elem.click()
                        time.sleep(1)
                        
                        text_xpaths = ['/html/body/ytcp-text-menu[4]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[7]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string',
                                       '/html/body/ytcp-text-menu[3]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[7]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string'
                                       '/html/body/ytcp-text-menu[2]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[7]',
                                       '/html/body/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[7]/ytcp-ve/tp-yt-paper-item-body/div/div/div']
                        
                        success = False
                        for xpath in text_xpaths:
                            try:
                                # text = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath',xpath))).text
                                text = driver.find_element('xpath',xpath).text
                                
                                # text = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath',text_xpaths[2]))).text
                              
                                if text == 'Appeal':
                                    statuses.append(solutions.pop(0).text) 
                                else:
                                    statuses.append('Pending')
                                success = True
                                break
                            except:
                                pass
                            
                        if not success:
                            try:
                                statuses.append(solutions.pop(0).text)
                            except:
                                statuses.append('Lost')
                                
                        ActionChains(driver).move_to_element(trigger).click().perform()
                    # print(statuses)
                    
                    if i==1: # A la primera, por motivos que no entiendo, no funciona pero a la segunda sí
                        list_of_claimers.append(claimers)
                        list_of_status.append(statuses)
                        list_of_content.append(claims)         
                
            else:
                try:
                    ActionChains(driver).move_to_element(triggers[0]).perform()
                    try:
                        target = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="slot-wrapper"]/ytcp-paper-tooltip-body/div/div[2]')))
                    except:
                        target = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="slot-wrapper"]/ytcp-paper-tooltip-body/div[2]')))
                    list_of_claimers.append(target.text)
                    
                    try:
                        status = driver.find_element('xpath','//*[@id="dispute-status"]')
                        list_of_status.append(status.text)
                        
                    except:
                        try:
                            driver.find_element('xpath','//*[@id="action-button"]').click() # Click 3 dots
                            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(('xpath', '//*[@id="text-item-6"]')))
                            list_of_status.append('Pending') 
                        except:
                            list_of_status.append('Lost')
                    
                    claim_item = driver.find_element('xpath','//*[@id="main"]/div/ytcp-animatable[19]/ytcr-video-home-page/ytcr-video-home-section/ytcr-video-content-list/div[2]/ytcr-video-content-list-claim-row/div[1]/div[2]/div[1]')
                    list_of_content.append(claim_item.text)
                except:
                    weird_ids.append(videoid)
                    list_of_claimers.append('a')
                    list_of_content.append('a')
                    list_of_status.append('a')
        except:
            passed_ids.append(videoid)
            list_of_claimers.append('a')
            list_of_content.append('a')
            list_of_status.append('a')
            pass # Nada que reclamar (????)
        
        
    
    
    new_data = pd.DataFrame({
        df.columns[0]: list_of_ids,
        df.columns[1]: list_of_titles,
        df.columns[2]: list_of_status,
        df.columns[3]: list_of_thumbs,
        df.columns[4]: list_of_claimers,
        df.columns[5]: list_of_content,
    })
    
    new_data = new_data[~new_data.videoid.isin(passed_ids)].reset_index(drop=True)
    new_data = new_data[~new_data.videoid.isin(weird_ids)].reset_index(drop=True)
    new_data['fecha'] = dt.datetime.today()
    
    df = pd.concat([df, new_data.reset_index(drop=True)], ignore_index=True)
    df = df.drop_duplicates(subset=df.columns[0], keep='last').reset_index(drop=True)
    df['status'] = df['status'].astype(str)
    df.to_excel(r'C:\Users\pablo.perezmartin\Documents\cleoycuquin\Automatizacion\Copyright_Claims.xlsx',index=False, engine='openpyxl')
    df.to_excel(r'A:\Automatizacion\Copyright_Claims.xlsx',index=False, engine='openpyxl')
    df.to_excel(r'\\cancer\Material_Definitivo\telerin\Copyright\Copyright_Claims.xlsx',index=False, engine='openpyxl')


# m = 0

# driver.get('https://studio.youtube.com/video/{}/copyright'.format(weird_ids[m]))
# m+=1

