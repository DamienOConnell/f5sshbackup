#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# needs doing:
#   What happens if the integrity checks on load_data fail?
#   Does it exit cleanly with a useful message?

from pprint import pprint
import sys
from netmiko import ConnectHandler, file_transfer
import socket
from socket import *


class CloudKey:
    def __init__(self, keydata: dict, mandatory: dict) -> None:

        """
        Check received data against mandatory fields.
        Initialize object data directly from dict.
        http://www.blog.pythonlibrary.org/2014/02/14/python-101-how-to-change-a-dict-into-a-class/
        """

        if not all(key in keydata for key in mandatory):
            print(f"Mandatory data field missing in data file.")
            exit(1)
        else:
            for item in keydata:
                setattr(self, item, keydata[item])

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        attrs = str([(x, self.__dict__[x]) for x in self.__dict__])
        return "<CloudKey: %s>" % attrs

    def open_connection(self):

        # "username", "password", "remote_path", "hostname", "local_path"
        #
        if self.password:  # public key auth
            try:
                self.connection = ConnectHandler(
                    device_type="linux",
                    ip=self.hostname,
                    username=self.username,
                    password=self.password,
                )
            except Exception:
                errormessage = "there was an error connecting to {}".format(self.hostname)
                sys.exit(errormessage)

    def close_connection(self):
        #
        # Check if connection is open before trying to close it
        #
        if hasattr(self, "connection"):
            print("Disconnecting ...")
            self.connection.disconnect()
        else:
            print("There is no connection, will not attempt to disconnect ...")

    def run_command(self, command: str) -> str:
        #
        # Check for working connection; open one before running command, if needed.
        #
        if not self.is_alive():
            #
            # USE LOGGER HERE
            #
            print("Opening connection, possibly for the first time...")
            self.open_connection()

        output = self.connection.send_command(command)
        return output

    def is_alive(self):

        null = chr(0)
        try:
            # Try sending ASCII null byte to maintain the connection alive
            self.connection.write_channel(null)
            return True
        except AttributeError as e:
            #
            # USE LOGGER HERE
            #
            print(f"Connection appears not to have been intialized yet ...")
            return False

        except Exception as e:
            # If unable to send, we can tell for sure that the connection is unusable
            #
            # USE LOGGER HERE
            #
            print(f"Unknown exception {e} cannot write over socket connection")
            return False
        return False
