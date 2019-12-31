import time
from selenium.webdriver import Chrome
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import streamlit as st
from urllib.parse import unquote
import requests
st.success("hi iam here to check thinks")


uri=st.text_input("enter url")
f = "sai"







if st.button("get"):


    options = Options()
    options.add_argument('--disable-infobars')
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options, port=9515)
    wait = WebDriverWait(driver, 10)


    driver.get(uri)
    for item in range(3):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(3)


    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
        f += (comment.text)
    st.success(f)
    driver.quit()


