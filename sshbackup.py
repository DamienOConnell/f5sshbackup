#!/usr/bin/env python3

import sys
import os
import argparse

# import time

from netmiko import ConnectHandler

# from paramiko import SSHClient
# from scp import SCPClient

# local
from logger import Logger
from dateops import dateTimeStamp
import scp_python

from md5 import checkmd5sum
import email_notify

MAX_USED_DISK = 51


def parse_df_output(df_output):
    """
        Return % free space extracted from df_output.
        Return 0 if this can't be extracted.
    """

    for line in df_output.splitlines():
        if line.endswith("/var") or line.endswith("/"):
            parts = line.split()
            if len(parts) > 6:
                # raise ValueError("Too many fields returned from df command")
                pass
            if parts[3].endswith("%"):
                result = int(parts[3].strip("%"))
                return result
            if parts[4].endswith("%"):
                result = int(parts[4].strip("%"))
                return result
    return 0


def get_args():
    parser = argparse.ArgumentParser(description="Backup F5 using SSH")
    parser.add_argument(
        "-t", "--targethost", help="device to be backed up", required=True
    )

    parser.add_argument("-u", "--username", help="login name", required=True)
    parser.add_argument(
        "-l", "--logfile", help="name of user specified log file", required=False
    )

    parser.add_argument(
        "-d", "--destpath", help="local path for backup file", required=False
    )

    # either device file, or device list are needed
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-p", "--password", help="device login password")
    source.add_argument("-i", "--sshid", help="ssh key to use for authentication")

    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-q", "--quiet", action="store_true")
    verbosity_group.add_argument("-v", "--verbose", action="store_true")

    return parser.parse_args()


def log_args(args, logger):
    """Write program arguments to logfile, using Logger object (logger.py)
    args is a namespace object, can't iterate over it directly"""

    for arg in vars(args):
        logger.debug("argument:  {}\tvalue:\t {}".format(arg, getattr(args, arg)))


def print_args(args):
    """print program arguments.
    args is a namespace object, can't iterate over it directly"""

    for arg in vars(args):
        print("argument:  {}\tvalue:\t {}".format(arg, getattr(args, arg)))


def new_archive_name(hostname):
    return hostname + "_" + dateTimeStamp() + ".tgz"


def new_f5_backup_filename(hostname):
    return hostname + "_" + dateTimeStamp() + ".ucs"


def main():

    #
    # 1 - SET ENVIRONMENT, GET & PARSE ARGS
    #

    # avoid absolute path to files - contacts, templates, esp. when using cron
    os.chdir(os.path.dirname(sys.argv[0]))

    args = get_args()

    if args.logfile:
        logfile = Logger(args.logfile)
    else:
        logfile = Logger("sshbackup.log")

    if args.verbose:
        print_args(args)
        log_args(args, logfile)

    f5_backup_filename = new_f5_backup_filename(args.targethost)

    # Need a try clause here
    if args.sshid:  # public key auth
        try:
            device = ConnectHandler(
                device_type="linux",
                ip=args.targethost,
                username=args.username,
                use_keys=True,
                key_file=args.sshid,
            )
        except Exception:
            errormessage = "there was an error connecting to {}".format(args.targethost)
            logfile.critical(errormessage)
            email_notify.send_error_message(
                "contacts.txt",
                "msg_failure.txt",
                args.targethost + " - BACKUP UNSUCCESSFUL",
                errormessage,
            )
            sys.exit(errormessage)

    elif args.password:  # password auth
        try:
            device = ConnectHandler(
                device_type="linux",
                ip=args.targethost,
                username=args.username,
                password=args.password,
            )
        except Exception:
            errormessage = "there was an error connecting to {}".format(args.targethost)
            logfile.critical(errormessage)
            email_notify.send_error_message(
                "contacts.txt",
                "msg_failure.txt",
                args.targethost + " - BACKUP UNSUCCESSFUL",
                errormessage,
            )
            sys.exit(errormessage)

    else:
        logfile.critical("No credentials, this won't work")
        sys.exit("No credentials, this won't work")

    if args.destpath:
        destpath = args.destpath
    else:
        destpath = "."

    #
    # 2 - GET DF ON APPLIANCE, PARSE, QUIT IF LOW
    #
    output = device.send_command("/bin/df /var/local/ucs/")
    logfile.info(output)
    usedspace = parse_df_output(output)

    if usedspace > MAX_USED_DISK:
        errormessage = "Destination disk {}% used, exceeds {}% limit ".format(
            usedspace, MAX_USED_DISK
        )
        logfile.critical(errormessage)
        email_notify.send_error_message(
            "contacts.txt",
            "msg_failure.txt",
            args.targethost + " - BACKUP SKIPPED",
            errormessage,
        )
        sys.exit(errormessage)
    else:
        logfile.info(
            "Disk space OK - {}% used on appliance backup path".format(usedspace)
        )

    #
    # 3 - BUILD SRC PATH
    #
    full_src_path = "/var/local/ucs/" + f5_backup_filename
    logfile.info("full_src_path {}".format(full_src_path))

    #
    # 4 RUN F5 BACKUP COMMAND
    #
    try:
        # using "device.send_command_expect" for longer running commands
        output = device.send_command_expect(
            "tmsh save /sys ucs " + full_src_path, max_loops=1000, delay_factor=20
        )
        logfile.info(output)
    except Exception:
        errormessage = "there was an error running backup command on host {}".format(
            args.targethost
        )
        logfile.critical(errormessage)
        email_notify.send_error_message(
            "contacts.txt",
            "msg_failure.txt",
            args.targethost + " - BACKUP UNSUCCESSFUL",
            errormessage,
        )
        sys.exit(errormessage)

    #
    # 5 - RUN MD5SUM ON F5, PARSE OUTPUT
    #
    output = device.send_command("/usr/bin/md5sum " + full_src_path)
    logfile.info("MD5SUM OUTPUT\n\n" + output)

    for line in output.splitlines():
        if line.endswith("ucs"):
            archive_md5, new_archive = line.split()
            logfile.info(
                "MD5 RESULT: {}; archive name: {}".format(archive_md5, new_archive)
            )

    #
    # 6 TRANSFER BACKUP FROM F5; REMOVE FROM F5
    #
    scp_python.get_file_scp(args.targethost, full_src_path, destpath)

    # clean up backup from the appliance
    output = device.send_command("/bin/rm -f " + full_src_path)

    logfile.info(
        "checkmd5sum() filename: " + f5_backup_filename + " MD5: " + archive_md5
    )

    # check the MD5 against what has been transferred
    if checkmd5sum(destpath + "/" + f5_backup_filename, archive_md5):
        logfile.info("MD5 check is True")
        md5_verified = True
    else:
        logfile.info("MD5 check is False")
        md5_verified = False

    print("APPLIANCE:    " + args.targethost)
    print("BACKUP FILE:  " + f5_backup_filename)
    print("BACKUP MD5:   " + archive_md5)
    print("MD5 VERIFIED: " + str(md5_verified))

    if md5_verified:
        logfile.info("F5 backup completed and verified")
        email_notify.send_mail_message(
            "contacts.txt",
            "msg_success.txt",
            args.targethost + " - backup successful",
            f5_backup_filename,
            archive_md5,
            usedspace,
        )
    else:
        errormessage = "F5 backup either not completed or could not be verified"
        logfile.info("F5 backup either not completed or not verified")
        email_notify.send_error_message(
            "contacts.txt",
            "msg_failure.txt",
            args.targethost + " - BACKUP UNSUCCESSFUL",
            errormessage,
        )


if __name__ == "__main__":
    main()
