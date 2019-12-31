import streamlit as st
import pandas as pd
from gensim.summarization import summarize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
import subprocess


#Chroumium packages
import time
from selenium.webdriver import Chrome
from contextlib import closing
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


import spacy
nlp=spacy.load('en_core_web_sm')
from spacy import displacy

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""



    



def Sumy_Summarize(docx): 
    parser= PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer=LexRankSummarizer()
    summary=lex_summarizer(parser.document,3)
    summary_list=[str(sentence) for sentence in summary]
    result=' '.join(summary_list)
    return result


@st.cache(allow_out_mutation=True)
def analyze_text(text):
    return nlp(text)

from bs4 import BeautifulSoup 
# from urllib.request import urlopen

@st.cache
def get_text(raw_url):
    f = []

    options = Options()
    options.add_argument('--disable-infobars')
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options, port=9515)
    wait = WebDriverWait(driver, 10)


    driver.get(raw_url)
    for item in range(3):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(3)


    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
        f.append(comment.text)
    driver.quit()


    return f



    

def main():
    st.title("Summary and Entity Checker")




    activities=["Summarizer","NER checker","NER for URL"]
    choice=st.sidebar.selectbox("Select Activity",activities)
    
    if choice== "Summarizer":
        st.subheader("Summary with NLP")
        raw_text=st.text_area("Exter Text Here","Type Here")
        summary_choice=st.selectbox("Summary Choice",["Gensim","Sumy Lex Rank"])
        if st.button("Summarize"):
            if summary_choice=='Gensim':
                summary_result=summarize(raw_text) 
            elif summary_choice=='Sumy Lex Rank':
                summary_result=Sumy_Summarize(raw_text)

            st.write(summary_result)
        


    if choice=='NER checker':
        st.subheader("Entity Recognition With Spacy")
        raw_text=st.text_area("Enter here","Type")
        if st.button("Analyze"):
            docx=analyze_text(raw_text)
            html=displacy.render(docx,style='ent')
            html=html.replace("\n\n","\n")
            st.write(html,unsafe_allow_html=True)
    
    if choice=='NER for URL':
        st.subheader("Analyze text from URL")
        raw_url=st.text_input("Enter URL","Type here")
        if st.button("Extract"):
            if raw_url!="Type here":
                result=get_text(raw_url)
                len_of_full_text=len(result)
                st.write(result)

            





if __name__ == "__main__":
    main() 