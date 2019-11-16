#!/usr/bin/env python3

import sys
import os
import argparse

from netmiko import ConnectHandler

from logger import Logger
import scp_python
from md5 import checkmd5sum, md5sum
import email_notify
from load_data import loadjson

# use load json routine to get all required parameters:
#
#   - username
#   - password
#   - remote host name / IP address
#   - remote path of archive
#   - local path for archive
#   - log file path and name (or use syslog)
#


def getargs():
    parser = argparse.ArgumentParser(description="Backup device using SSH")

    parser.add_argument("-l", "--logfile", help="user specified log file", required=False)
    parser.add_argument("-c", "--config", help="user specified log file", required=True)

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-q", "--quiet", action="store_true")
    verbosity_group.add_argument("-v", "--verbose", action="store_true")

    return parser.parse_args()


def main():

    #
    # allows relative path for files, esp. when using cron
    os.chdir(os.path.dirname(sys.argv[0]))
    args = getargs()

    print(args)
    variables = loadjson(args.config)
    for v in variables:
        print(f"Variable {v} == {variables[v]}")



if __name__ == "__main__":
    main()
