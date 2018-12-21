from zipfile import ZipFile
from glob import glob
import os
PATH = "/home/vinicios/Downloads/teste"

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
        files = glob(self.path+"/*.zip")
        files.sort(key=os.path.getmtime, reverse=True)
        print files
        cont = 0
        for station in stations:
            for file in files:
                if file.endswith(".zip") and belongs_to_station(file, station):
                    print str(cont) +"conte"
                    cont = cont +1
                    zip = ZipFile(os.path.join(PATH, file))
                    zip.extractall(PATH)
                    self.concatenate(station)
            old_file = os.path.join(self.path, "temp.csv")
            new_file = os.path.join(self.path, str(station+".csv"))
            print(old_file+" "+new_file)
            os.rename(old_file, new_file)

    def concatenate(self, station):
        print "huehueheuehueh"
        output = open(self.path+"/temp.csv", "w+")
        files = glob(self.path+"/*.csv")
        files.sort(key=os.path.getmtime, reverse=True)
        skip = 0
        for file in files:
            if file.endswith(".csv") and belongs_to_station(file, station):
                f = open(file, "r+")
                for line in f:
                    if skip:
                        skip = 0
                    else:
                        self.lista.append(line)
                skip = 1
                f.close()
                # os.remove(os.path.join(PATH, file))

        output.write("".join(self.lista))
        output.close()
