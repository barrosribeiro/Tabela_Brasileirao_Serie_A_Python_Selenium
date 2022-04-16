# Bibliotecas --------------------------------------------------
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import csv

# Author: Leonardo Ribeiro
# Github: https://github.com/barrosribeiro
# Consulta Tabela Brasileirão Série A - 2022

# Tabela Classificação - Times
def ClassficacaoTimes(driver):

    element = driver.find_element_by_xpath("/html/body/div[2]/main/div[2]/div/section[1]/article/section[1]/div/table[1]")
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    times = soup.find_all('strong', {'class':'classificacao__equipes classificacao__equipes--nome'})

    lista = []
    for time in times:
        lista.append(time.text)

    df = pd.DataFrame(lista, columns=['Times'])

    return df

# Tabela Brasileirão completa
def TabelaBrasileirao():
    
    url = "https://ge.globo.com/futebol/brasileirao-serie-a/"

    option = Options()
    option.headless = True
    driver = webdriver.Firefox()

    driver.get(url)
    time.sleep(15)
    df_class = ClassficacaoTimes(driver)
 
    element = driver.find_element_by_xpath("/html/body/div[2]/main/div[2]/div/section[1]/article/section[1]/div/table[2]")
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find_all(name='table')

    df_full = pd.read_html(str(table))[0]

    df = pd.DataFrame(df_full, columns=['P', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', '%', 'ÚLT. JOGOS'])
    df = pd.concat([df_class, df], axis=1, join='outer')

    df.to_csv(r'./Tabela_Brasileirao_A_2022.csv', index = False)
    
    driver.quit()

# Chamada da função inicialização -->
if __name__ == '__main__':
    TabelaBrasileirao()
 


