from zipfile import ZipFile
from glob import glob
from preprocessing import *
import os

PATH = "/home/vinicios/Downloads/telemetria2"
home = os.path.expanduser('~')
PATH = os.path.join(home, "Downloads","telemetria3")
OUTPUT_PATH = os.path.join(home,"Downloads","datasets")
id_estacoes = ["67100000", "66960008", "66825000", "66810000", "66125000"]
def belongs_to_station(file, station):
    if file.find(station) < 0:
        return False
    return True

class Unzip():
    def __init__(self, path, stations):
        self.path = path
        self.stations = stations
        self.lista = []

    def decompress(self, stations=None):
        if stations == None:
            stations = self.stations
        # print("decompress path", self.path)
        files = glob(self.path+"/*.zip")
        files.sort(key=os.path.getmtime, reverse=True)
        # print files
        cont = 0
        for station in stations:
            for file in files:
                if file.endswith(".zip") and belongs_to_station(file, station):
                    cont = cont +1
                    zip = ZipFile(os.path.join(self.path, file))
                    zip.extractall(self.path)
                    self.concatenate(station)
            old_file = os.path.join(self.path, "temp.csv")
            new_file = os.path.join(self.path, str(station+".csv"))
            os.rename(old_file, new_file)
            self.lista = []

    def concatenate(self, station):
        if os.path.isfile(self.path+"/temp.csv"):
            os.remove(self.path+"/temp.csv")
        output = open(self.path+"/temp.csv", "w")
        files = glob(self.path+"/*.csv")
        files.sort(key=os.path.getmtime, reverse=True)
        skip = 1
        for file in files:
            # print(file)
            if file.endswith(".csv") and belongs_to_station(file, station):
                f = open(file, "r+")
                for line in f:
                    # print("line",line)
                    if skip:
                        skip = 0
                    else:
                        self.lista.append(line)
                skip = 1
                f.close()
                # os.remove(os.path.join(PATH, file))
        # print(self.lista)
        output.write("".join(self.lista))
        output.close()

if __name__ == '__main__':
    unzip = Unzip(PATH, id_estacoes)
    unzip.decompress()
    for station in id_estacoes:
        # print(station)
        filename = station+".csv"
        do_process(OUTPUT_PATH, filename)
