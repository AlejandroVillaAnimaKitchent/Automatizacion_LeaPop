from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle



options = Options()
# options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.5735.110')

driver = webdriver.Chrome(options=options) 
driver.get('https://www.youtube.com/')

pickle.dump( driver.get_cookies() , open("pages/cookies_cyber.pkl","wb"))
#pickle.dump( driver.get_cookies() , open("pkls/cookies_cyber.pkl","wb"))