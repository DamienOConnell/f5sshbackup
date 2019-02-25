# f5sshbackup
```
Syntax:
    usage: sshbackup.py [-h] -t TARGETHOST -u USERNAME [-l LOGFILE] [-d DESTPATH]
                        (-p PASSWORD | -i SSHID) [-q | -v]

    Backup F5 using SSH

    optional arguments:
      -h, --help            show this help message and exit
      -t TARGETHOST, --targethost TARGETHOST
                            device to be backed up
      -u USERNAME, --username USERNAME
                            device login user
      -l LOGFILE, --logfile LOGFILE
                            user specified log file
      -d DESTPATH, --destpath DESTPATH
                            local path for transferred file
      -p PASSWORD, --password PASSWORD
                            device login password
      -i SSHID, --sshid SSHID
                            ssh key to use for authentication
      -q, --quiet
      -v, --verbose
```

Backup F5 devices using SSH.  
F5 devices don't have an inbuilt archiving mechanism.  

1. Script runs manually or from cron.  
2. F5 configuration is saved on the appliance.  
3. Disk space is checked to ensure there is adequate disk space to continue. 
4. Configuration is saved to an archive with naming 
  <hostname>_yyyy-mm-dd_HH-MM
5. MD5 is calculated for the saved archive.  
6. Archive is retrieved to chosen directory. 
7. MD5 is calculated for the retrieved file.
8. Mail message is sent to advise success or failure of these processes, md5sum and disk space free in %.  
