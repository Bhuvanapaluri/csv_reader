import csv
import os
from datetime import datetime
import decimal


files_path = 'csv_files/'
output_csv = 'final_data.csv'
fp = None
fp_writer = None


def is_date(val):
    try:
        x = int(val)
        return False
    except:
        try:
            x = float(val)
            return False
        except:
            if val.isalpha(): return False
            return True

def get_date(val):
    return_format = '%Y-%m-%d'
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%b %d, %Y', '%b %d %Y', '%d-%m-%Y','%d %b %Y']
    for f in formats:
        try:
            dt = datetime.strptime(val,f).strftime(return_format)
            return dt
        except:
            continue
        
def is_type(val):
    if val.isalpha():return True
    else: return False

def get_data(data):
    global fp_writer
    flag = True
    to_col = None
    from_col = None
    for row in data:
        record = [None, None, 0.0, None, None]
        if flag:
            flag = False
            for i, col in enumerate(row):
                if col == 'to': to_col = i
                if col == 'from': from_col = i
            continue
        amount_flag = False
        for i, col in enumerate(row):
            if i == to_col: record[3] = col
            elif i == from_col: record[4] = col
            elif is_date(col):
                date = get_date(col)
                record[0] = date
            elif is_type(col):
                record[1] = col
            else:
                x = decimal.Decimal(col)
                if amount_flag:
                    x = record[2] + decimal.Decimal(col) * decimal.Decimal(0.1)
                amount_flag = True
                record[2] = x.quantize(decimal.Decimal('.01'))

        fp_writer.writerow(record)
            
        

def main():
    global fp_writer
    

    files = [file for file in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, file))]
    with open('final_data.csv', 'w', newline='') as fp:
        fp_writer = csv.writer(fp)
        fp_writer.writerow(['date', 'type', 'amount', 'to', 'from'])
        for file in files:
            with open(files_path + '/' + file, 'r') as f:
                data = csv.reader(f)
                get_data(data)

main()



