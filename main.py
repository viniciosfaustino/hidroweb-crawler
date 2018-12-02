# -*- coding: utf-8 -*-
import time
import os
from crawler import *
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


id_estacoes = ["67100000", "66970000", "66960008", "66825000", "66810000", "66125000", "66750000"]
nomes_estacoes = ["PORTO MURTINHO", "FORTE COIMBRA", "PORTO ESPERANCA", "LADARIO (BASE NAVAL)", "SAO FRANCISCO", "BELA VISTA DO NORTE", "PORTO DO ALEGRE"]
#forte coimbra e porto alegre não tem informacoes telemetricas


# ID_ESTACAO = '47001000'
# NOME_ESTACAO = 'PORTO - TRAVESSIA DA BALSA'
date = ["13/11/1950", "13/12/1950"]
# for i in range(len(id_estacoes)):
#     download_hidroweb(id_estacoes[i], nomes_estacoes[i], home, date)

error_message = "Não existe medições cadastrada para a estação selecionada"

current_year = time.localtime().tm_year
for year in reversed(xrange(1990, current_year+1)):
    print(year)
    for month in reversed(xrange(1,13)):
        dtInicio = "01/"+str(month-1)+"/"+str(year)
        dtFinal = "01/"+str(month)+"/"+str(year)
        dt = (dtInicio, dtFinal)
        for i in range(len(id_estacoes)):
            driver = create_driver()
            if month == 1:
                dtInicio = "01/"+str(12)+"/"+str(year-1)
                dtFinal = "01/"+str(month)+"/"+str(year)
                dt = (dtInicio, dtFinal)
            print("Iniciando "+nomes_estacoes[i])
            download_hidroweb(driver, id_estacoes[i], nomes_estacoes[i], home, dt)
            print("finalizando "+nomes_estacoes[i])

            print
            driver.quit()
