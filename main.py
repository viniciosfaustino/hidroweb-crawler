# -*- coding: utf-8 -*-
import time
import os
from driver import create_driver
from crawler import Crawler
import sys
#from pyvirtualdisplay import Display

id_estacoes = ["67100000", "66970000", "66960008", "66825000", "66810000", "66125000", "66750000"]
nomes_estacoes = ["PORTO MURTINHO", "FORTE COIMBRA", "PORTO ESPERANCA", "LADARIO (BASE NAVAL)", "SAO FRANCISCO", "BELA VISTA DO NORTE", "PORTO DO ALEGRE"]
#forte coimbra e porto alegre não têm informacoes telemetricas
home = os.path.expanduser('~')

if (len(sys.argv) > 1):
    download_path = sys.argv[1]
else:
    download_path = os.path.join(home, "Downloads")

error_message = "Não existe medições cadastrada para a estação selecionada"
crawler = Crawler()
current_year = time.localtime().tm_year
for year in reversed(range(1990, current_year+1)):
    for month in reversed(range(1,13)):
        print(year, month)
        dtInicio = "01/"+str(month-1)+"/"+str(year)
        dtFinal = "01/"+str(month)+"/"+str(year)
        dt = (dtInicio, dtFinal)
        for i in range(len(id_estacoes)):
            driver = create_driver(download_path)
            if month == 1:
                dtInicio = "01/"+str(12)+"/"+str(year-1)
                dtFinal = "01/"+str(month)+"/"+str(year)
                dt = (dtInicio, dtFinal)
            print("Iniciando "+nomes_estacoes[i])
            crawler.download_hidroweb(driver, id_estacoes[i], nomes_estacoes[i], download_path, dt)
            print("finalizando "+nomes_estacoes[i])

            print("\n")
            driver.quit()
