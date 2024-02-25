# Grab power on info using Python scripting

import argparse
import os

from cmd2 import Cmd, Cmd2ArgumentParser, with_argparser


class cli(Cmd):
    def __init__():
        super().__init__()


argparser = Cmd2ArgumentParser()

def main():
    cli.cmdloop()


if __name__ == "__main__":
    main()

# smartctl /dev/sdg -d megaraid,1 -x
