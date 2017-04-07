from fabric.api import run,env,execute,hosts,hide,settings,cd,sudo,put
from fabric.operations import sudo
from fabric.decorators import runs_once, parallel
from fabric.tasks import execute
from fabric.network import ssh

import paramiko, os
paramiko.util.log_to_file("filename.log")

env.forward_agent = True
env.use_ssh_config = True

NAGIOS_CORE_VERSION = "4.3.1"
NAGIOS_CORE_PACKAGE = "nagios-{}".format(NAGIOS_CORE_VERSION)
NAGIOS_CORE_URL = "https://assets.nagios.com/downloads/nagioscore/releases/{package}.tar.gz".format(package=NAGIOS_CORE_PACKAGE)

env.hosts = ['edb-nagios']

def upgradeNagios():
         run('hostname')
         execute(backupNagios)
         sudo('mkdir tmp')
         with cd('~/tmp'):
              run('pwd')
              run('sudo wget {}'.format(NAGIOS_CORE_URL))
              run('sudo tar -xvzf nagios-{}.tar.gz'.format(NAGIOS_CORE_VERSION))
              run('sudo rm nagios-{}.tar.gz'.format(NAGIOS_CORE_VERSION))
              with cd('nagios-{}'.format(NAGIOS_CORE_VERSION)):
                   run('pwd')
                   run_with_settings("sudo ./configure --with-nagios-group=nagcmd")
                   sudo("make all")
                   sudo("make install")
                   run('sudo service nagios configtest')
                   run('sudo service nagios configtest | grep "Nagios Core 4"') 
                   sudo('rm -R ~/tmp')
                   with cd('~/'):
                        execute(restoreBackupNagios)
                        sudo('rm -r usr/')
                        run('sudo service nagios configtest')
                        run('sudo service nagios restart')

def run_with_settings(command):
    return run(command.format(**globals()))


def backupNagios():
              run('./backup_nagios')

def restoreBackupNagios():
              run('tar -xvof *_etc_backup*.tar.gz')
              with cd('~/usr/local/nagios/etc/'):
                   run('ls -la')
                   run('ls -la /usr/local/nagios/etc')
                   sudo('cp -R * /usr/local/nagios/etc')
                   sudo('chown -R nagios:nagios /usr/local/nagios/etc')
                   run('pwd && ls -la /usr/local/nagios/etc')
