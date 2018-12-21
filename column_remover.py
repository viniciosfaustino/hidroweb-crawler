import csv
import time
import datetime
def remove_extra_columns(filename):
    with open(filename,"rb") as source:
        rdr= csv.reader( source,delimiter=";" )
        with open(str("clean"+filename),"wb") as result:
            wtr = csv.writer( result,delimiter=";" )
            for r in rdr:
                wtr.writerow( (r[0], r[3]) )

def get_day_mean(filename):
    result = {}
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        skip = 1
        for row in csvreader:
            if not skip:
                if row[0] in result:
                    result[row[0]].append(int(row[1]))
                else:
                    result[row[0]] = [int(row[1])]
            else:
                skip = 0

        for k in result.keys():
            # print result[k]
            result[k] = sum(result[k])/int(len(result[k]))
    csvfile.close()

    with open(str("new"+filename),'wb') as f:
        w = csv.writer(f,delimiter=";")
        w.writerows(result.items())
    f.close()
    print result


def datetime_to_timestamps(filename):
    result = []
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        for row in csvreader:
            timestamp = time.mktime(datetime.datetime.strptime(row[0], '%d/%m/%Y').timetuple())
            result.append([int(timestamp), row[1]])

        csvfile.close()

    print result
    with open(str("new_"+filename),'wb') as f:
        w = csv.writer(f,delimiter=" ")
        for r in result:
            print r[0], r[1]
            w.writerow(r)

    f.close()
