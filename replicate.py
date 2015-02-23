#!/usr/bin/python

##############################################
# Si les tables ne sont pas creees sur la base
# de destination, penser a preciser un fichier
# en 4eme argument.
##############################################

import os
import sys
import subprocess
from subprocess import call

#Check des args
if len(sys.argv) < 4 :
    print 'Usage : ./replicate.py src dest tbl1,tbl2,tbl3 [to_execute.sql]'
    exit (1)

#Infos diverses
FNULL = open(os.devnull, 'w')
orig_base = sys.argv[1];
dest_base = sys.argv[2]
tables = sys.argv[3].split(",");
sql_file_name = sys.argv[4];
file_name = orig_base+'_to_'+dest_base+'.ini'
job_name = orig_base+'_to_'+dest_base

#Couleurs SHELL
class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def write_file():
#Lignes du fichier
    f_header = '[londiste]\n'
    f_job_name = 'job_name = '+job_name+'\n'
    f_provider = 'provider_db = dbname='+orig_base+'\n'
    f_subscriber = 'subscriber_db = dbname='+dest_base+'\n'
    f_pgq = 'pgq_queue_name = '+job_name+'\n'
    f_logfile = 'logfile = /tmp/%(job_name)s.log\n'
    f_pidfile = 'pidfile = /tmp/%(job_name)s.pid\n'
    f = open(file_name, 'w')
    f.write(f_header + f_job_name + f_provider + f_subscriber + f_pgq + f_logfile + f_pidfile)

def exec_sql():
    cmd = 'psql '+dest_base+' -f' + sql_file_name
    call(cmd, stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

def install_londiste_provider():    
    cmd = 'londiste ' + './' +file_name+ ' provider install'
    call(cmd, stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
def install_londiste_subscriber():
        cmd = 'londiste ' + './' +file_name+ ' subscriber install'
        call(cmd, stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
def config_londiste_provider():
    for t in tables :
        cmd = 'londiste ' + './' +file_name+ ' provider add ' + t
        call(cmd, shell=True)
def config_londiste_subscriber():
    for t in tables :
        cmd = 'londiste ' + './' +file_name+ ' subscriber add ' + t
        call(cmd, shell=True)

print 'Les tables suivantes seront repliquees depuis la base '+ c.FAIL + orig_base.upper() + c.ENDC + ' vers la base ' + c.OKGREEN + dest_base.upper() + c.ENDC + ' : '
for t in tables:
    print('public.'+t)
cnt = raw_input('Faut-il poursuivre ? y/n\n')
if cnt == 'y' or cnt == 'Y' :
    cnt = True;
else:
    exit (1)

print c.WARNING + '[Verification de l\'existence des BDD :',
out_orig = subprocess.check_output('psql -l | grep -w '+orig_base+' | wc -l', shell=True)
if out_orig == '1\n':
    print c.ENDC + c.OKGREEN + orig_base + c.ENDC + c.WARNING + ' OK',
else :
        print c.ENDC + c.FAIL + '\t Not ok...]' + c.ENDC
        exit (1)
out_dest = subprocess.check_output('psql -l | grep -w '+dest_base+' | wc -l', shell=True)
if out_dest == '1\n':
    print c.ENDC + c.OKGREEN + dest_base + c.ENDC + c.WARNING + ' OK]'
else :
    print c.ENDC + c.FAIL + '\t Not ok...]' + c.ENDC
    exit (1)
write_file();
print c.WARNING + '[Generation du fichier de configuration... \t OK] : ' +c.ENDC + c.OKGREEN + file_name + c.ENDC 
install_londiste_provider()
print c.WARNING + '[Installation de londiste sur '+c.OKGREEN+orig_base+c.WARNING+'... \t\t OK]' +c.ENDC
install_londiste_subscriber()
print c.WARNING + '[Installation de londiste sur '+c.OKGREEN+dest_base+c.WARNING+'... \t\t OK]' +c.ENDC
config_londiste_provider()
print c.WARNING + '[Pensez a creer la table sur '+c.ENDC + c.OKGREEN + dest_base+ c.ENDC + c.WARNING + ': \n\t\tCreation des table(s) \t\t OK]' +c.ENDC
exec_sql()
print c.WARNING + '[Renseignement des tables a repliquer... \t OK]' + c.ENDC
config_londiste_subscriber()
print 'Lancer la replication avec : $: londiste '+file_name+' replay -d'

