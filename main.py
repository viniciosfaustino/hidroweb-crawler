# -*- coding: utf-8 -*-
import time
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

options = Options()
options.set_headless(headless=True)

from selenium.webdriver.common.keys import Keys

home = os.path.expanduser('~')

def wait_load_items(driver, xpath):

    n = 1
    p = 1
    while p:
        try:
            driver.find_element_by_xpath(xpath)
            p = 0
        except:
            print(n, xpath)
            time.sleep(1)
            n += 1
        if n == 300:
            print('Tempo de espera excedito. Processo encerrado.')
            exit()

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


def create_driver():
    fp = webdriver.FirefoxProfile()

    options.set_preference("browser.download.folderList",2)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.focusWhenStarting", False)
    # options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.download.dir", '/home/vinicios/Downloads/bilada')

    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.download.manager.alertOnEXEOpen", False)
    options.set_preference("browser.download.manager.closeWhenDone", True)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
    options.set_preference("pdfjs.disabled", True)

    driver = webdriver.Firefox(firefox_options=options,executable_path='/opt/geckodriver')

    return driver

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
            exit()

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
            exit()
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
            return()
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
        print "alert done"
        er = False
        try:
            #verify if there is data of informed date
            driver.find_element(By.XPATH, '//li[contains(text(),"Não existe medições cadastrada para a estação selecionada.")]')
            print "Sem medicões para a data"
            er = True
            return()
        except:
            pass
        print er
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
                exit()
    except Exception as e:
        print(e)
    # driver.quit()
    # print("oe")


id_estacoes = ["67100000", "66970000", "66960008", "66825000", "66810000", "66125000", "66750000"]
nomes_estacoes = ["PORTO MURTINHO", "FORTE COIMBRA", "PORTO ESPERANCA", "LADARIO (BASE NAVAL)", "SAO FRANCISCO", "BELA VISTA DO NORTE", "PORTO DO ALEGRE"]
#forte coimbra e porto alegre não tem informacoes telemetricas


# ID_ESTACAO = '47001000'
# NOME_ESTACAO = 'PORTO - TRAVESSIA DA BALSA'
date = ["13/11/1950", "13/12/1950"]
# for i in range(len(id_estacoes)):
#     download_hidroweb(id_estacoes[i], nomes_estacoes[i], home, date)

error_message = "Não existe medições cadastrada para a estação selecionada"

day = 1
current_year = time.localtime().tm_year
for year in reversed(xrange(1990, current_year+1)):
    print(year)
    for month in xrange(3,13):
        dtInicio = str(day)+"/"+str(month-2)+"/"+str(year)
        dtFinal = str(day)+"/"+str(month)+"/"+str(year)
        dt = (dtInicio, dtFinal)
        for i in range(len(id_estacoes)):
            driver = create_driver()
            download_hidroweb(driver, id_estacoes[i], nomes_estacoes[i], home, dt)
            print("finished "+nomes_estacoes[i])
