# metrics_collector
Server manager using cmd2. 

## Supported Features
 - smartctl SMART monitoring
 - rsync backup

## Dependencies
 - Python 3.11
 - uv
 - cmd2 2.4.3
 - black
 - isort

## Setup

```bash
uv sync
```

For development tools:

```bash
uv sync --group dev
```

## Usage

```bash
sudo uv run metrics-collector
```

## Commands

### status
options:
* -d \<number>: Display smart data for specific disk number

### backup

options:
* user@host:data_dir/: Remote user, host and data directory
* --dry-run: Perform a trial run with no changes made

