import os

import pandas
import json
import csv


'''maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)
'''


def csv_to_json(data):
    jsonfile = open('../Generated Data/data.json', 'w')
    reader = csv.reader(data)
    fieldnames = []
    for row in reader:
        fieldnames.append(row[0])
    fieldnames = fieldnames[0:15]
    csvfile = open('../Sources/data.csv', 'r')
    reader2 = csv.DictReader(csvfile, fieldnames)
    next(reader2)
    next(reader2)

    for row in reader2:
        # print(row)
        json.dump(row, jsonfile)
        jsonfile.write('\n')


def get_df_from_csv(name = "data_clean.csv",n = None,colonne=None):
    ROOT_DIR = os.path.dirname(os.path.abspath("app.py"))
    data = pandas.read_csv(ROOT_DIR+"/Sources/"+name, sep=',', low_memory=False, nrows=n)
    # # data.fillna("NoData", inplace=True)  # Replace the null value by a string "NoData"
    df = pandas.DataFrame(data)

    df = df.drop_duplicates(subset=["Date", "From", "To", "content"], keep="first", ignore_index=True)
    if colonne is not None:
        df = df[colonne]
    return df