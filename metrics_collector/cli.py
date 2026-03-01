# Grab power on info using Python scripting

import argparse
import os
import readline
import re
import subprocess

import cmd2


class MetricsCollector(cmd2.Cmd):
    PRSYNC_PATH = os.path.join(os.path.dirname(__file__), "prsync")
    HISTORY_LIMIT = 100

    cmd2.Cmd.prompt = "metrics_collector> "
    intro = "Welcome to MetricsCollector. Type help or ? to list commands.\n"

    arg_parser = cmd2.Cmd2ArgumentParser()
    arg_parser.add_argument("-d", type=int, help="drive ID")
    arg_parser.add_argument("--dry-run", action="store_true", help="dry run")

    def __init__(self):
        super().__init__()
        self.history_file = os.path.join(
            os.path.expanduser("~"), ".local", "state", "metrics_collector", "history"
        )
        self._history_save_error_reported = False
        self._init_history()

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
        rsync_env = dict(os.environ)
        rsync_env["RSYNC_RSH"] = "/usr/bin/ssh -T -c aes128-ctr -o Compression=no -x"

        if args.dry_run:
            rsync = subprocess.Popen(
                [
                    self.PRSYNC_PATH,
                    "--parallel=4",
                    "-aAXvP",
                    "--delete",
                    "--dry-run",
                    "--progress",
                    "--exclude=/dev/*",
                    "--exclude=/proc/*",
                    "--exclude=/sys/*",
                    "--exclude=/var/tmp/*",
                    "--exclude=swapfile",
                    "--exclude=lost+found",
                    "--exclude=.cache",
                    "/",
                    str(user_dest),
                ],
                stdout=subprocess.PIPE,
                env=rsync_env,
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
                        self.PRSYNC_PATH,
                        "--parallel=4",
                        "-aAXvP",
                        "--delete",
                        "--progress",
                        "--exclude=/dev/*",
                        "--exclude=/proc/*",
                        "--exclude=/sys/*",
                        "--exclude=/var/tmp/*",
                        "--exclude=swapfile",
                        "--exclude=lost+found",
                        "--exclude=.cache",
                        "/",
                        str(user_dest),
                    ],
                    stdout=subprocess.PIPE,
                    env=rsync_env,
                )
                while True:
                    line = rsync.stdout.readline().decode("utf-8")
                    if not line:
                        break
                    self.poutput(line)
            else:
                self.poutput("Backup cancelled")

    def postcmd(self, stop, statement):
        self._save_history()
        return stop

    def postloop(self):
        self._save_history()
        super().postloop()

    def _init_history(self):
        history_dir = os.path.dirname(self.history_file)
        os.makedirs(history_dir, exist_ok=True)

        if os.path.isfile(self.history_file):
            try:
                readline.read_history_file(self.history_file)
            except OSError:
                pass

        readline.set_history_length(self.HISTORY_LIMIT)

    def _save_history(self):
        try:
            readline.set_history_length(self.HISTORY_LIMIT)
            readline.write_history_file(self.history_file)
        except OSError as ex:
            if not self._history_save_error_reported:
                self.perror(f"Unable to save history to {self.history_file}: {ex}")
                self._history_save_error_reported = True


def main():
    import sys

    if not os.geteuid() == 0:
        sys.exit("Script must be run as root")
    cli = MetricsCollector()
    sys.exit(cli.cmdloop())


if __name__ == "__main__":
    main()
