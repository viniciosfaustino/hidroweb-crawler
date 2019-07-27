# -*- coding: utf-8 -*-

## esse script deveria verificar com uma frequencia informada, os valores dos níveis dos rios da lista informada
#o processo deveria ter o seguinte fluxo:
#dada uma estação de coleta, o script faria verificações periódicas sobre o nível do rio.
#com o arquivo baixado, deveria ser feito todo o pré processamento para o formato usado pelo modelo de ML
#em seguida dar um append no arquivo com o histórico dos rios
#ficar em idle enquanto não estiver pegando dados telemétricos


import time
import os
from driver import create_driver
from crawler import Crawler
import sys
from unzip import Unzip
from datetime import date
from preprocess import *

home = os.path.expanduser('~')
SOURCE_PATH = os.path.join(home, "Downloads", "hidroweb", "medidas")
OUTPUT_PATH = os.path.join(home, "Downloads","hidroweb", "datasets")

def add_new_measure(source_path, dataset_path, station):
    #ao inves de alterar arquivos, idealmente uma lista vai ser passada como parâmetro para as funções
    path = source_path
    # print("path add new measure: ", path)
    unzip = Unzip(path, [station])
    unzip.decompress([station])
    filename = station+".csv"
    output = pre_process(path, filename)
    path = dataset_path
    file = os.path.join(dataset_path, filename)
    append_measure(file, output)


if __name__ == '__main__':
    while(1):
        start = time.time()

        id_estacoes = ["67100000", "66970000", "66960008", "66825000", "66810000", "66125000", "66750000"]
        nomes_estacoes = ["PORTO MURTINHO", "FORTE COIMBRA", "PORTO ESPERANCA", "LADARIO (BASE NAVAL)", "SAO FRANCISCO", "BELA VISTA DO NORTE", "PORTO DO ALEGRE"]
        home = os.path.expanduser('~')

        if (len(sys.argv) > 1):
            download_path = sys.argv[1]
        else:
            download_path = SOURCE_PATH

        error_message = "Não existe medições cadastrada para a estação selecionada"
        crawler = Crawler()
        current_year = time.localtime().tm_year

        today = date.today()
        dtInicio = today.strftime("%d/%m/%Y")
        dtFinal = dtInicio
        dt = (dtInicio, dtFinal)
        for i in range(len(id_estacoes)):
            driver = create_driver(download_path)
            print("Iniciando "+nomes_estacoes[i])
            status = crawler.download_hidroweb(driver, id_estacoes[i], nomes_estacoes[i], download_path, dt)
            print("finalizando "+nomes_estacoes[i])
            print("\n")
            driver.quit()
            if status > -1:
                add_new_measure(SOURCE_PATH, OUTPUT_PATH, id_estacoes[i])

            #aqui deve ser chamada uma função que descompacta os arquivos e realiza o append no dataset
        elapsed = time.time() - start
        print("Aguardando próxima medição")
        time.sleep(24*3600 - elapsed)
