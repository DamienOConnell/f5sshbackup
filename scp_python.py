#!/usr/bin/env python3

from paramiko import SSHClient
from scp import SCPClient


def get_file_scp(srchost, srcfile, dstfile):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    # ssh.connect(srchost, username="admin", pkey="id_rsa")
    ssh.connect(srchost, username="admin")
    # SCPCLient takes a paramiko transport as an argument
    scp = SCPClient(ssh.get_transport())
    scp.get(srcfile, dstfile)
    scp.close()


def main():
    print("testing scp transfer from srchost to dstfile)
    srchost = "myf501"
    srcfile = "/var/local/ucs/myf5_26_9_2018_LH.ucs"
    dstfile = "/var/tmp/."
    get_file_scp(srchost, srcfile, dstfile)


if __name__ == "__main__":
    main()
