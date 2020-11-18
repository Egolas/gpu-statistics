# GPU statistics
## Requests
- gpustat
- mysql-connector-python

## Usage
Adding the script to system crontab, to report GPU statistics every minute.

1. Edit `host_name` and `database_config` in `gpu-statistics.py`
2. Edit `filepath` in `log_gpustat.sh`
3. Edit crontab configuration of system with cmd `crontab -e`
4. In the new edit window, (if you are editting crontab for the first time, system will ask to select the editor), add task with the following text (append to the last line), in which filepath is the same with `log_gpustat.sh`:
> */1 * * * * ${filepath}/gpu-statistics/log_gpustat.sh


