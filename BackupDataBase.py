#!/usr/bin/env python
# 2014-05-21 15:48:14 pingliangchenisthebest@gmail.com
# Copyright (c) 2009, PinLiang Chen'. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import sys
import os
import time
import datetime
import paramiko
from daemon import runner
from threading import Thread
from collections import defaultdict
from collections import Counter
BackupPath = 'your local path'
RemotePath = 'your remote path'
DB_user = 'your database user name'
DB_passwd = 'your database password'
DB_name = 'your database name'
Host = 'Remote IP'
Port = 22
User = 'Romote user name'
Passwd = 'Remote password'

def BackupDatabase():
    if not os.path.exists(BackupPath):
        os.makedirs(BackupPath)

    date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d@%H:%M:%S')
    dumpcmd = "mysqldump --user=" + DB_user +" --password=" + DB_passwd + " "+ DB_name +" > " + BackupPath + date + ".sql"
    os.system(dumpcmd)

    transport = paramiko.Transport((Host, Port))
    transport.connect(username = User, password = Passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(BackupPath+date+".sql", RemotePath+date+".sql")
    sftp.close
    transport.close()
    print 'Finish'
        

class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/BackupDatabase.pid'
        self.pidfile_timeout = 5

    def run(self):
        while True:
            BackupDatabase()
            time.sleep(604800) # One Week

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
