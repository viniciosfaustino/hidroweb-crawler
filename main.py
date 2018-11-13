# -*- coding: utf-8 -*-
import time
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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

def download_hidroweb(id_station, name_estation, dir_out):

	# display = Display(visible=0, size=(800,600))
	# display.start()

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
	wait_load_items(driver, '//div[contains(@class, "checkbox i-checks")]')
	time.sleep(2)
	try:
		driver.find_element_by_xpath('//div[contains(@class, "checkbox i-checks")]').click()
	    	click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesC\\:radTipoArquivo-componente > div:nth-child(2) > div:nth-child(2)')
	    	click_css_selector(driver, '#form\\:fsListaEstacoes\\:fsListaEstacoesC\\:btBaixar')
	except Exception as e:
		print(e)



id_estacoes = ["67100000", "66970000", "66960008", "66825000", "66810000", "66125000", "66750000", ]
nomes_estacoes = ["PORTO MURTINHO", "FORTE COIMBRA", "PORTO ESPERANCA", "LADARIO (BASE NAVAL)", "SAO FRANCISCO", "BELA VISTA DO NORTE", "PORTO DO ALEGRE"]

# ID_ESTACAO = '47001000'
# NOME_ESTACAO = 'PORTO - TRAVESSIA DA BALSA'
for i in range(len(id_estacoes)):
    download_hidroweb(id_estacoes[i], nomes_estacoes[i], home)
