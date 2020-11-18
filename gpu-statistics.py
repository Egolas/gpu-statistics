import os
import json
import time
from mysql_utils import auto_insert_database

host_name = 'hostname' # input your hostname

# input database config
database_config = {
    'user': 'user',
    'password': 'password',
    'host': '0.0.0.0',
    'database': 'gpustat',
    'raise_on_warnings': True,
    'auth_plugin': 'caching_sha2_password'
}

def read_stat():
    cmd = 'gpustat -cu --no-color --json'
    stat = os.popen(cmd).read()
    stat_json = json.loads(stat)
    return stat_json

def get_records(stats):
    records = []
    timestamp = time.time()
    for gpu in stats['gpus']:
        for process in gpu['processes']:
            record = {
                'timestamp':timestamp,
                'hostname':host_name,
                'username':process['username'],
                'memory.usage':process['gpu_memory_usage'],
                'gpu.index':gpu['index'],
                'gpu.name':gpu['name'],
                'gpu.memory.total':gpu['memory.total']
            }
            records.append(record)
    return records

def main():
    stats = read_stat()
    stats_dict = get_records(stats)
    for record in stats_dict:
        auto_insert_database(database_config, record, table='gpustatistics')

if __name__ == '__main__': 
    main()

