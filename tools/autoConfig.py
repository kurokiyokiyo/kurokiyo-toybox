import sys
import pexpect
import getpass
from datetime import datetime

class Logger(object):
    def __init__(self, hostname):
        self.terminal = sys.stdout
        self.log = open("./log/" + "log_" + hostname +"_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log","w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        pass  

class deviceConnector:
    def __init__(self):
        self.child = None
        self.login_prompt=[
                     r".*\#{1,1}\s*$|.*\>{1,1}\s*$",
                     r"[p|P]assword\:.*$",
                     r"\(yes\/no\).*$",
                     r"Permission denied.*",
        ]
    def login(self, hostname, username, passwd):
        child = pexpect.spawnu("ssh -l "+username+" "+hostname, maxread=4000, searchwindowsize=100)
        sys.stdout = Logger(hostname)
        child.logfile_read = sys.stdout
        index = child.expect(self.login_prompt)
        while True:
            print(index)
            if index == 0: #success
                self.child = child
                return True
            elif index == 1: # need to input password
                child.sendline(passwd)
                index = child.expect(self.login_prompt)
            elif index == 2: # need to input password
                child.sendline("yes")
                index = child.expect(self.login_prompt)
            elif index == 3: # need to input password
                print("Password Incorrect or Permission deny")
                return False
            else: #error
                print("error")
                return False
    def send_config(self, configs):
        for c in configs:
            self.child.sendline(c.strip())
            self.child.expect(self.login_prompt[0])
        self.child.close()

def autoConfig(username, password, hostfile, configfile):
    hostlist = []
    configlist = []
    confirm = ""
    #print hostfile
    try:
        for host in open(hostfile,"r"):
            hostlist.append(host),
    except:
        print("can not open host list!")
        exit()
        
    try:
        for config in open(configfile,"r"):
            configlist.append(config)
    except:
        print("can not open config!")
        exit()

    print("#### device confirm ####")
    for host in hostlist:
        print(host,end=""),
    print("Device OK?[y/n] : ",end=""),
    confirm = input()
    if confirm != "y" and confirm != "Y":
        print("abort")
        exit()

    print("#### config confirm ####")
    for config in configlist:
        print(config,end=""),
    print("Config OK?[y/n] : ",end=""),
    confirm = input()
    if confirm != "y" and confirm != "Y":
        print("abort")
        exit()

    for host in hostlist:
        print("Executing ...." + host)
        c = deviceConnector()
        if c.login(host.strip(),username.strip(),password.strip()):
            c.send_config(configlist)
            pass

if __name__ == '__main__':
    argvs = sys.argv
    print(argvs)
    if len(argvs) != 3:
        print("usage : python autoConfig.py [hostnamefile] [configfile]")
        exit()
    print("please input username: ",end="")
    username = input()
    password = getpass.getpass('please input password: ',)
    autoConfig(username, password, sys.argv[1], sys.argv[2] )
