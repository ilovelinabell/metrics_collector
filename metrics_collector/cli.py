# Grab power on info using Python scripting

import subprocess
import re
import argparse

import cmd2

class MetricsCollector(cmd2.Cmd):
    cmd2.Cmd.prompt = "metrics_collector> "
    intro = "Welcome to MetricsCollector. Type help or ? to list commands.\n"

    arg_parser = cmd2.Cmd2ArgumentParser()
    arg_parser.add_argument('-d', type=int, help='drive ID')

    @cmd2.with_argparser(arg_parser)
    def do_status(self, args):
        if args.d >= 0 and args.d <= 7:
            ssdinfo = subprocess.run(["smartctl", "-a", "/dev/sdg", "-d", "megaraid," + str(args.d)], stdout=subprocess.PIPE)
            sections = re.split(r"===.*===", ssdinfo.stdout.decode('utf-8'), maxsplit=3)
            info, read = sections[1], sections[2]
            vendor_specific_attributes = re.split(r"SMART Error Log Version: \d", re.split(r"SMART Attributes Data Structure revision number: \d", read)[1])[0]
            self.poutput(info)
            self.poutput(vendor_specific_attributes)

if __name__ == "__main__":
    import sys
    cli = MetricsCollector()
    sys.exit(cli.cmdloop())
