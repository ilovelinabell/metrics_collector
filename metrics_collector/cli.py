# Grab power on info using Python scripting

import argparse
import os
import re
import subprocess

import cmd2


class MetricsCollector(cmd2.Cmd):
    cmd2.Cmd.prompt = "metrics_collector> "
    intro = "Welcome to MetricsCollector. Type help or ? to list commands.\n"

    arg_parser = cmd2.Cmd2ArgumentParser()
    arg_parser.add_argument("-d", type=int, help="drive ID")
    arg_parser.add_argument("--dry-run", action="store_true", help="dry run")

    @cmd2.with_argparser(arg_parser)
    def do_status(self, args):
        if args.d >= 0 and args.d <= 7:
            ssdinfo = subprocess.run(
                ["smartctl", "-a", "/dev/sdg", "-d", "megaraid," + str(args.d)],
                stdout=subprocess.PIPE,
            )
            sections = re.split(r"===.*===", ssdinfo.stdout.decode("utf-8"), maxsplit=3)
            info, read = sections[1], sections[2]
            vendor_specific_attributes = re.split(
                r"SMART Error Log Version: \d",
                re.split(r"SMART Attributes Data Structure revision number: \d", read)[
                    1
                ],
            )[0].lstrip()
            self.poutput(info)
            self.poutput(vendor_specific_attributes)

    @cmd2.with_argparser(arg_parser)
    def do_backup(self, args):
        user_dest = self.read_input("user@destination:directory> ")
        if not user_dest:
            self.perror("rsync destination not specified")
            return

        if not re.match(r"^\w+@[\w.]+:[\w/]+$", user_dest):
            self.perror("Invalid path")
            return

        self.poutput("Backing up data to " + user_dest)
        if args.dry_run:
            rsync = subprocess.Popen(
                [
                    "rsync",
                    "-azAXvP",
                    "--delete",
                    "--dry-run",
                    "--exclude=/dev/*",
                    "--exclude=/proc/*",
                    "--exclude=/sys/*",
                    "--exclude='swapfile'",
                    "--exclude='lost+found'",
                    "--exclude='.cache'",
                    "/",
                    str(user_dest),
                ],
                stdout=subprocess.PIPE,
            )
            while True:
                line = rsync.stdout.readline().decode("utf-8")
                if not line:
                    break
                self.poutput(line)
        else:
            confirm = self.read_input("Please confirm this action (y/n)> ")
            if confirm == "y":
                rsync = subprocess.Popen(
                    [
                        "rsync",
                        "-azAXvP",
                        "--delete",
                        "--exclude=/dev/*",
                        "--exclude=/proc/*",
                        "--exclude=/sys/*",
                        "--exclude='swapfile'",
                        "--exclude='lost+found'",
                        "--exclude='.cache'",
                        "/",
                        str(user_dest),
                    ],
                    stdout=subprocess.PIPE,
                )
                while True:
                    line = rsync.stdout.readline().decode("utf-8")
                    if not line:
                        break
                    self.poutput(line)
            else:
                self.poutput("Backup cancelled")


if __name__ == "__main__":
    import sys

    if not os.geteuid() == 0:
        sys.exit("Script must be run as root")
    cli = MetricsCollector()
    sys.exit(cli.cmdloop())
