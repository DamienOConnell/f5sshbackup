#!/usr/bin/env python3

import argparse
from netmiko import ConnectHandler


def listFromCLI(argument):
    """
    Given a comma separated list of commands, return a list
    """
    argument = argument.strip()
    commandlist = list(argument.split(","))
    return commandlist


def listFromFile(filename):
    """
    Given the name of a file containing something, one per line, return a list
    of strings
    """
    newlist = []
    with open(filename, mode="r", encoding="utf-8") as inputfile:
        for line in inputfile:
            item = line.strip()
            newlist.append(item)

    return newlist


def main():
    parser = argparse.ArgumentParser(
        description="F5 backup over SSH connection, username or certificate authenticaion."
    )

    parser.add_argument("-u", "--username", help="device login user", required=True)
    parser.add_argument("-p", "--password", help="device login password", required=True)

    # one of device file, or device list are needed
    deviceSource = parser.add_mutually_exclusive_group(required=True)
    deviceSource.add_argument("-f", "--file", help="device listing file")
    deviceSource.add_argument(
        "-d", "--device", help="comma separated list of devices to connect to"
    )

    commandSource = parser.add_mutually_exclusive_group()
    commandSource.add_argument(
        "-e",
        "--execute",
        help="Comma separated list of commands to run on targets, quote if they contains any spaces",
    )

    commandSource.add_argument(
        "-c",
        "--commandfile",
        help="File with commands to run on targets, one per line.",
    )

    verbosityGroup = parser.add_mutually_exclusive_group()
    verbosityGroup.add_argument("-q", "--quiet", action="store_true")
    verbosityGroup.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        print("Verbose")
    if args.quiet:
        print("Not verbose")

    if args.execute:
        commandList = listFromCLI(args.execute)
    else:
        if args.commandfile:
            commandList = listFromFile(args.commandfile)
        else:
            commandList = listFromCLI("/bin/ls -la")
    #
    #
    # How to insert a Ctrl-C catcher in the loop?
    #
    if args.device:
        deviceList = listFromCLI(args.device)

    if args.file:
        deviceList = listFromFile(args.file)

    for host in deviceList:
        host = host.strip()
        device = ConnectHandler(
            device_type="f5_ltm",
            ip=host,
            username=args.username,
            password=args.password,
        )
        for command in commandList:
            output = device.send_command(command)
            print(output)


if __name__ == "__main__":
    main()
