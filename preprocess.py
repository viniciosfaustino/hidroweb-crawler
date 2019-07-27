import csv
import time
import datetime
import os
def remove_extra_columns(path,filename):
    output = []
    # print("caminho remove",os.path.join(path, filename))
    with open(os.path.join(path, filename),"rb") as source:
        rdr= csv.reader(source,delimiter=";" )
        # with open(str(path+"/clean"+filename),"wb") as result:
        #     wtr = csv.writer( result,delimiter=";" )
        for r in rdr:
            # print("r ",r)
            output.append([r[0], r[3]])
    source.close()
    # print("output remove extra columns", output)
    return output

def get_day_mean(data):
    # print("data ",data)
    result = {}
    skip = 1
    output = []
    for row in data:
        # if not skip:
        try:
            int(row[1])
            # print("row: ",int(row[1]))
            if row[0] in result:
                result[row[0]].append(int(row[1]))
            else:
                result[row[0]] = [int(row[1])]
        except ValueError:
            # print("vesh")
            if row[0] in result:
                result[row[0]].append(0)
            else:
                result[row[0]] = [0]

        else:
            skip = 0
    for k in result.keys():
        # print('oi')
        result[k] = sum(result[k])/int(len(result[k]))
        output.append([k, result[k]])
    # print("result after get_day_mean: ", output, "\n")
    return output


def datetime_to_timestamps(data):
    result = []
    for row in data:
        timestamp = time.mktime(datetime.datetime.strptime(row[0], '%d/%m/%Y').timetuple())
        result.append([int(timestamp), row[1]])
    result = sorted(result, key=lambda x: x[0], reverse=False)
    # print("result after datetime_to_timestamps: ", result, "\n")
    return result

def append_measure(filepath, data):
    data = data[0]
    # print("data final",data)
    if (len(data)>0):
        file = open(filepath, "a+")
        row = str(data[0])+" "+str(data[1])
        # print(data)
        file.write(row)
        file.close()


def pre_process(path, filename):
    data = remove_extra_columns(path, filename)
    # print("pre process data", data)
    # remove_extra_columns(path,filename)
    data = get_day_mean(data)
    # print("get day mean data", data)
    output = datetime_to_timestamps(data)
    return output
