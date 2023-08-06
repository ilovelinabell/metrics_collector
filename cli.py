# An interactive command line interface for ClickHouse database through Python

import argparse
import os

import clickhouse_connect
from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser


class cli(Cmd):
    def __init__():
        super().__init__()


argparser = Cmd2ArgumentParser()


def Secrets():
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    storage_path = os.getenv("CLICKHOUSE_STORAGE_PATH", "/var/lib/clickhouse/")
    log_path = os.getenv("CLICKHOUSE_LOG_PATH", "/var/log/clickhouse-server/")
    return dict({"host": host, "storage_path": storage_path, "log_path": log_path})


def main():
    secrets = Secrets()

    print(f'podman run --rm --network=host --user 1000:10\
        -v {secrets.get("storage_path")}:/var/lib/clickhouse/ \
        -v {secrets.get("log_path")}:/var/log/clickhouse-server/ \
        clickhouse/clickhouse-server:latest')

    ret = os.system(
        f'podman run --rm --network=host --user 1000:10\
        -v {secrets.get("storage_path")}:/var/lib/clickhouse/ \
        -v {secrets.get("log_path")}:/var/log/clickhouse-server/ \
        clickhouse/clickhouse-server:latest'
    )

    if ret:
        raise RuntimeError("Error: could not start ClickHouse server")

    metrics_collector = cli()

    try:
        client = clickhouse_connect.get_client(secrets.get("host"))
    except:
        print("WARNING: Could not connect to ClickHouse DB")
    metrics_collector.intro = "Welcome to the ClickHouse Metrics Collector. Type help or ? to list commands.\n"
    metrics_collector.prompt = "ClickHouseMetricsCollector> "
    cli.cmdloop()


if __name__ == "__main__":
    main()
