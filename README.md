# metrics_collector
Server manager using cmd2. 

## Supported Features
 - smartctl SMART monitoring
 - rsync backup

## Dependencies
 - Python 3.11
 - Poetry 1.5.1
 - cmd2 2.4.3
 - black
 - isort

 ## Usage
 ```bash
 sudo python3 metrics_collector.py
 ```

## Commands

### status
options:
* -d \<number>: Display smart data for specific disk number

### backup

options:
* user@host:data_dir/: Remote user, host and data directory
* --dry-run: Perform a trial run with no changes made

