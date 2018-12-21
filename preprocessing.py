import csv
import time
import datetime
def remove_extra_columns(path,filename):
    with open(path+"/"+filename,"rb") as source:
        rdr= csv.reader( source,delimiter=";" )
        with open(str(path+"/clean"+filename),"wb") as result:
            wtr = csv.writer( result,delimiter=";" )
            for r in rdr:
                wtr.writerow( (r[0], r[3]) )

def get_day_mean(path,filename):
    result = {}
    with open(path+"/clean"+filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        skip = 1
        for row in csvreader:
            if not skip:
                try:
                    int(row[1])
                    if row[0] in result:
                        result[row[0]].append(int(row[1]))
                    else:
                        result[row[0]] = [int(row[1])]
                except ValueError:
                    if row[0] in result:
                        result[row[0]].append(0)
                    else:
                        result[row[0]] = [0]

            else:
                skip = 0

        for k in result.keys():
            result[k] = sum(result[k])/int(len(result[k]))
    csvfile.close()

    with open(str(path+"/new"+filename),'wb') as f:
        w = csv.writer(f,delimiter=";")
        w.writerows(result.items())
    f.close()


def datetime_to_timestamps(path,filename):
    result = []
    with open(path+"/new"+filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        for row in csvreader:
            timestamp = time.mktime(datetime.datetime.strptime(row[0], '%d/%m/%Y').timetuple())
            result.append([int(timestamp), row[1]])

        csvfile.close()
    result = sorted(result, key=lambda x: x[0], reverse=False)
    with open(str(path+"/new_"+filename),'wb') as f:
        w = csv.writer(f,delimiter=" ")
        for r in result:
            w.writerow(r)

    f.close()

def do_process(path,filename):
    remove_extra_columns(path,filename)
    get_day_mean(path,filename)
    datetime_to_timestamps(path,filename)
