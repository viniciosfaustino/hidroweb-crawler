# -*- coding: utf-8 -*-
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

import os
import time
home = os.path.expanduser('~')

def wait_load_items(driver, xpath):

    n = 1
    p = 1
    while p:
        try:
            driver.find_element_by_xpath(xpath)
            p = 0
        except:
            # print(n, xpath)
            time.sleep(1)
            n += 1
        if n == 300:
            print('Tempo de espera excedito. Processo encerrado.')
            driver.quit()
            return

def click_css_selector(driver, css_selector):
    n = 0
    p = 1
    while p:
        try:
            driver.find_element_by_css_selector(css_selector).click()
            p = 0
        except:
            time.sleep(1)
            n += 1

        if n == 300:
            print('Tempo de espera excedido.')
            break

def download_hidroweb(driver, id_station, name_estation, dir_out, date):

    # display = Display(visible=0, size=(800,600))
    # display.start()
    dtInicio, dtFinal = date

    url = 'http://www.snirh.gov.br/hidroweb/publico/apresentacao.jsf'
    driver.get(url)
    time.sleep(1)
    driver.get(url)
    n = 0
    p = 1
    while  p:
        try:
            driver.find_element_by_link_text('Séries Históricas').click()
            p = 0
        except:
            time.sleep(1)
            n += 1
        if n == 300:
            print('Tempo de espera excedido. Processo encerrado.')
            driver.quit()
            return

    wait_load_items(driver, '//*[@id="form:fsListaEstacoes:codigoEstacao"]')
    driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:codigoEstacao"]').send_keys([id_station, Keys.ENTER])
    wait_load_items(driver, '//*[@id="form:fsListaEstacoes:nomeEstacao"]')
    driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:nomeEstacao"]').send_keys([name_estation, Keys.ENTER])
    click_css_selector(driver, '#form\\:fsListaEstacoes\\:bt')
    p = 1
    n = 0
    while  p:
        try:
            driver.find_element_by_link_text('Dados Telemétricos').click()
            p = 0
        except:
            time.sleep(1)
            n += 1
        if n == 300:
            print('Tempo de espera excedido. Processo encerrado.')
            driver.quit()
            return
    wait_load_items(driver, '//div[contains(@class, "checkbox i-checks")]')
    time.sleep(2)
    wait_load_items(driver, '//div[contains(@class, "checkbox i-checks")]')
    try:
        # dtInicio = "13/08/2018"
        # <p>Nenhum registro encontrado</p>
        try:
            #verify if there is data of informed date
            driver.find_element(By.XPATH, '//p[contains(text(),"Nenhum registro encontrado")]')
            print("Nenhum registro encontrado")
            # driver.close()
            try:
                driver.quit()
            except:
                print("deu ruim, amizade")
            return
        except:
            pass

        # driver.find_element_by_xpath('//*[@id="form:fsListaEstacoes:fsListaEstacoesT:dtInicio"]').clear()
        script = "document.getElementById('form:fsListaEstacoes:fsListaEstacoesT:dtInicio').setAttribute('value','"+dtInicio+"')"
        driver.execute_script(script);
        # dtFinal = "13/11/2018"
        script = "document.getElementById('form:fsListaEstacoes:fsListaEstacoesT:dtFinal').setAttribute('value','"+dtFinal+"')"
        driver.execute_script(script);

        click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesT\\:j_idt268\\:table\\:0\\:ckbSelecionadaT')
        click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesT\\:radTipoArquivoT-componente > div:nth-child(2) > div:nth-child(2)')
        click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesT\\:btGerarArquivoTel')
        p = 1
        n = 0
        wait_load_items(driver, '//li[contains(@class, "alert alert-info")]')
        try:
            #verify if there is data of informed date
            driver.find_element(By.XPATH, '//li[contains(text(),"Não existe medições cadastrada para a estação selecionada.")]')
            print "Sem medicões para a data"
            er = True
            driver.quit()
            return
        except:
            pass
        while  p:
            try:
                click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesT\\:btBaixar')
                p = 0
                # print "abaixo temos um teste para ver o que eh obangs"
                # print driver.find_element(By.XPATH, '//li[text()="Não existe medições cadastrada para a estação selecionada"]')
                # click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesT\\:btGerarArquivoTel')
                driver.quit()
            except:
                n += 1
            if n == 300:
                print('Tempo de espera excedido. Processo encerrado.')
                driver.quit()
                return
                # exit()
    except Exception as e:
        print(e)
    driver.quit()
    # print("oe")
