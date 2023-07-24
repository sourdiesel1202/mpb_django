import datetime
import json, csv, os
import multiprocessing
import time
from zoneinfo import ZoneInfo


def load_module_config(module):
    print(f"Loading config file for {module}")
    with open(f"configs/{module}.json", "r") as f:
        return json.loads(f.read())

def write_csv(filename, rows):
    with open(filename  , 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    # print(f"output file written to {filename}")
    # global_workbook.sheets.append('reports/sheets/'+filename)
def read_csv(filename):
    result = []
    with open(filename,'r', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in spamreader:
            result.append([x for x in row])
    return  result
def delete_csv(filename):
    os.system(f"rm {filename}")
    # print(f"Deleted file {filename}")

def generate_csv_string(rows):
    filename = f"tmp{datetime.datetime.now().month}{datetime.datetime.now().day}{datetime.datetime.now().year}{datetime.datetime.now().minute}{datetime.datetime.now().second}{os.getpid()}.csv"
    write_csv(filename,rows)
    res = ""
    with open(filename, "r") as f:
        res = f.read()
    delete_csv(filename)
    return res
def combine_csvs(files):
    _filestr = '\n'.join(files)
    # print(f"Combining the following files {_filestr}")
    records = []
    for _file in files:
        rows= read_csv(_file)
        if len(records) == 0:
            records.append(rows[0])

        for i in range(1, len(rows)):
            records.append(rows[i])
        delete_csv(_file)
    return records
def get_today(module_config, minus_days=0):

    if module_config['test_mode']:
        d = datetime.datetime.strptime(module_config['test_date'], "%Y-%m-%d")
    else:
        d=  datetime.datetime.now()
    if minus_days > 0:
        return (d - datetime.timedelta(days=minus_days)).strftime("%Y-%m-%d")
    else:
        return d.strftime("%Y-%m-%d")
def calculate_percentage(x, y):
    try:
        return (float(x)/float(y))*100.00
    except:
        return 0.0
def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp) / 1e3, tz=ZoneInfo('US/Eastern'))#.strftime("%Y-%m-%d %H:%M:%S")

def human_readable_datetime(_d):
    return _d.strftime("%Y-%m-%d %H:%M:%S")
def process_list_concurrently(data, process_function, batch_size):
    '''
    Process a list concurrently
    :param data: the list to process
    :param process_function: the function to pass to the multiprocessing module
    :param batch_size: the number of records to process at a time
    :return: None
    '''
    _keys = [x for x in data]
    n = batch_size
    loads = [_keys[i:i + n] for i in range(0, len(_keys), n)]
    # for load in loads:
    #     load.insert(0, data[0])
    # for load in loads:
    #     print(f"Load size: {len(load)}")
    # return
    processes = {}
    for load in loads:
        # p = multiprocessing.Process(target=process_function, args=(load,))
        p = multiprocessing.Process(target=process_function, args=(load,))
        p.start()

        processes[str(p.pid)] = p
    pids = [x for x in processes.keys()]
    while any(processes[p].is_alive() for p in processes.keys()):
        # print(f"Waiting for {len([x for x in processes if x.is_alive()])} processes to complete. Going to sleep for 10 seconds")
        process_str = ','.join([str(v.pid) for v in processes.values() if v.is_alive()])
        print(f"The following child processes are still running: {process_str}")
        time.sleep(10)
    return pids