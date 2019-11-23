#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#

from cloudkey import *
from load_data import loadjson


def line(length: int) -> None:
    print("-" * length)


def main():

    cloud_data = loadjson("data.json")
    mandatory = ["username", "password", "remote_path", "hostname", "local_path"]
    ck_instance = CloudKey(cloud_data, mandatory)

    line(132)
    print(ck_instance)
    line(132)

    output = ck_instance.run_command("/bin/ls -la /home/")
    print(output)

    # can't do this until the filename is appended to the path
    fl = ck_instance.get_file_list()   
    for f in fl:
        print(f"nextfile {f}")
    if len(fl)  > 0:
        print(f"last file is: {fl[-1]}")
        print(f"last file full path: {ck_instance.remote_path +  fl[-1]}")
        # testfile = ck_instance.remote_path +  fl[-1]
        # print(f"Getting last file: {testfile}")
        ck_instance.get_file_scp(fl[-1])
 
    ck_instance.close_connection()


if __name__ == "__main__":
    main()
