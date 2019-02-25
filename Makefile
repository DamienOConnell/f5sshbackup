run:
	./sshbackup.py -v -t myf503 -u admin -i /home/username/.ssh/id_rsa -l debug.log -d /var/backup

f5:
	./sshbackup.py -v -t myf501 -u admin -i /home/username/.ssh/id_rsa -l debug.log -d /var/backup
	./sshbackup.py -v -t myf502 -u admin -i /home/username/.ssh/id_rsa -l debug.log -d /var/backup
	./sshbackup.py -v -t myf501 -u admin -i /home/username/.ssh/id_rsa -l debug.log -d /var/backup
	./sshbackup.py -v -t myf502 -u admin -i /home/username/.ssh/id_rsa -l debug.log -d /var/backup

edit:
	vim ./sshbackup.py Makefile *py
