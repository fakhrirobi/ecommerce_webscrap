

# import keras
# import numpy as np 

# from keras import models,layers

import selenium 
from selenium import webdriver



import base64
import streamlit as st 
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import asyncio
import pandas as pd
import selenium 
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException,InvalidArgumentException,StaleElementReferenceException
from time import sleep 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import numpy as np 
import seaborn as sns
from webdriver_manager.chrome import ChromeDriverManager
pd.set_option('display.max_colwidth',None)



@st.cache
def query (product) : 
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    gChromeOptions.add_argument("disable-dev-shm-usage")
    

    prefs = {"profile.default_content_setting_values.notifications" : 2}
    gChromeOptions.add_experimental_option("prefs",prefs)
    gDriver = webdriver.Chrome(chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install())
    gDriver.get(f"https://www.tokopedia.com/search?st=product&q={product}")
    hasil_query = {}
    other_info = []
    try : 
        items = WebDriverWait(gDriver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="css-18c4yhp"]')))
        

        price = WebDriverWait(gDriver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="css-rhd610"]')))
        harga = [x.text for x in price]
        barang = [x.text for x in items]
        item_data = zip(barang,harga)
        # total_pages = driver.find_element_by_xpath('//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[5]/div[2]/div/button[10]')
        # query_result = driver.find_element_by_xpath('//*[@id="zeus-root"]/div/div[2]/div/div[2]/div[2]/div[1]')
        hasil_query['barang'] = barang
        hasil_query['harga'] = harga
        # other_info.append(total_pages.text)
        # other_info.append(query_result.text)
    except (NoSuchElementException,StaleElementReferenceException) : 
        print('gaada')

    df = pd.DataFrame(hasil_query)
    return df
def download_file(dataframe,filename) : 
    excel = dataframe.to_csv()
    b64 = base64.b64encode(excel.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV Query Result</a> (right-click and save as &lt;some_name&gt;.csv)'
    return st.sidebar.markdown(href, unsafe_allow_html=True)
    



        
        
        

if __name__ == '__main__' : 
    ######################SIDEBAR###################################
    st.sidebar.title(''' MARKET PRICE SCRAPER APP''')
    st.markdown('This application trace  the price of stuff in online marketplace')
    y = st.sidebar.text_input('enter the stuff you want to search')
    #checkbox = st.sidebar.selectbox('Please Select Types of file you want to download the query result :',('Excel','CSV','JSON','SQL'))
    #st.sidebar.button('CLick to download the file')
    
    filename= st.sidebar.text_input('please input filename for download without extension')
    #button = st.sidebar.button('Click to download csv ')
    data = query(y)
    

    ###########creating statistics from your search######################
    #price range
    st.title(r'We will show you the search result as soon as possible')
    data_copy = data.copy(deep=True)
    data_copy['harga'] = data_copy['harga'].str.replace('Rp','')
    data_copy['harga'] = data_copy['harga'].str.replace('.','')
    data_copy['harga'] = [float(x) for x in data_copy['harga'] ]

    min_price  = data_copy['harga'].min()
    min_price = f'{min_price:,}'
    max_price = data_copy['harga'].max()
    max_price = f'{max_price:,}'
    avg_price = np.average(data_copy['harga'])
    avg_price = f'{avg_price:,}'

    prog_bar = st.progress(0)
    for percent in range(100) : 
        time.sleep(0.00001)
        prog_bar.progress(percent+1)

    st.text('The Result of your Search')
    st.text('Minimum Price for %s %s' %(y.upper(),max_price))
    st.text('minimum price %s %s' %(y.upper(),min_price))
    st.text('average price %s %s' %(y.upper(),avg_price))
    st.write(data)
    st.text('Here Is the plot of your item')
    fig = sns.displot(data_copy)
    st.pyplot(fig)

    download_file(data,filename)
