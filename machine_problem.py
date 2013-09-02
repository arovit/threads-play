#!/usr/bin/python

import os
import random
import time
import threading

ALIVE_FILE = "alive"
WORKDIR = "" # to be assigned
RECOVER_TIME = 2 
MACHINEMAP = {}  
N_ALIVEMACHINES = 0 


def machine_operation(cmd):
    """ Machine operation - add/delete alive file - need to be thread safe"""
    threadLock.acquire()
    os.system(cmd)
    threadLock.release()


def count_machines_down():
    global N_ALIVEMACHINES
    N_ALIVEMACHINES = len([i for i in MACHINEMAP if os.path.exists(MACHINEMAP[i].path+'/'+ALIVE_FILE)])


class AliveCount(threading.Thread):
    
    """ Thread to count alive machine every second """
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
 
    def run(self):
        while True: 
            count_machines_down()
            #print N_ALIVEMACHINES
            time.sleep(self.counter)
    

class MachineDestroyer(threading.Thread):

    """ Thread to delete alive files from machine """ 
    def __init__(self, counter, perc):
        threading.Thread.__init__(self)
        self.counter = counter
        self.fail_perc = perc 
 
    def run(self):
        while True:
            destroy_machines(destroy_choose_machine(self.fail_perc))
            time.sleep(self.counter)

    
class Recovery(threading.Thread):
 
    """ Recovery thread. Spawn when a object in destroyed """

    def __init__(self, name, counter): 
        threading.Thread.__init__(self)
        self.name = name 
        self.counter = counter

    def run(self):
        time.sleep(self.counter)
        cmd = 'touch %s/%s'%(self.name, ALIVE_FILE)
        machine_operation(cmd)
        ##print "recovered " + self.name
        
    
class Machine:

    """" Class to simulate a machine """

    def __init__(self, path):
        cmd = 'mkdir %s;touch %s/%s'%(path, path, ALIVE_FILE)
        machine_operation(cmd)
        self.set_location(path)
        pass

    def set_location(self, path):
        self.path = path

    def get_location(self):
        return self.path

    def destroy(self):
        cmd = 'rm %s/%s'%(self.path, ALIVE_FILE) 
        machine_operation(cmd)
        #print "%s is down"%(self.path) 
        thread = Recovery(self.path, RECOVER_TIME)
        thread.start()

    def __repr__(self):
        return self.get_location()         


def destroy_machines(maclist):
    """ Delete the alive file inside the machine dir """
    global MACHINEMAP 
    path = os.getcwd()
    os.chdir(WORKDIR)
    for mac in maclist:
        mobj = MACHINEMAP.get(mac)
        mobj.destroy() 
    os.chdir(path) 


def destroy_choose_machine(pmachines):
    """ Apply the random sampling to get list of machines """
    mlen = len(MACHINEMAP.keys())
    samples = (pmachines*mlen)/100
    randlist = random.sample(MACHINEMAP.keys(), samples)
    return randlist


def setup(machines, pmachines, recover):
    """
    Initiate creating dirs and alive file 
    """
    global WORKDIR
    global MACHINEMAP
    global RECOVER_TIME
    os.system('rm -rf m_*')
    RECOVER_TIME = recover 
    WORKDIR = os.path.dirname(os.path.abspath(__file__))
    for i in xrange(machines):
	file_path = WORKDIR + "/m_"+str(i+1)
        MACHINEMAP[i+1] = Machine(file_path)


def add_machines(mlist):
    mlist = map(int, mlist)
    for i in mlist:
        if i in MACHINEMAP.keys():
            print "Machine %s already existing . Skiping. "%i  
            continue
        else:
	    file_path = WORKDIR + "/m_"+str(i)
            MACHINEMAP[i] = Machine(file_path) 
            print "Machine %s added "%file_path 

def remove_machines(mlist):
    mlist = map(int, mlist)
    for i in mlist:
        if not i in MACHINEMAP.keys():
            print "Machine %s not added yet . Skiping. "%i
            continue
        else:
            print "Removed Machine %s"%MACHINEMAP[i].get_location()
            del MACHINEMAP[i]

def is_alive(mac):
    mac = int(mac) 
    try: 
       if os.path.exists(MACHINEMAP[mac].get_location()+'/'+ALIVE_FILE):
           return True
    except:
       return False 
    return False 

def get_input():
    """ 
    N - machines
    f - Perc of machine failing every 5 seconds
    t - Number of second to recover
    """
    machines = input("No of machines : ")
    pmachines = input("Percentage of machines failing every 5 seconds : ")
    recover = input("Number of seconds to recover for a machine : ")
    setup(machines, pmachines, recover)
    destroyer_thread = MachineDestroyer(5, pmachines) # THREAD - 1  Destory machines 
    destroyer_thread.daemon = True
    destroyer_thread.start()
    alive_count_thread = AliveCount(1)    # THREAD - 2 Count machines
    alive_count_thread.daemon = True
    alive_count_thread.start()
    inpstring = ''
    while 'quit' not in inpstring:
        inpstring = raw_input('>')
        try:
            if 'add_machines' in inpstring:   # SYNTAX : add_machines 5,6,7,8 <integers>
                args = inpstring.split('add_machines')[1].strip().split(',')
                add_machines(args)
            elif 'remove_machines' in inpstring:
                args = inpstring.split('remove_machines')[1].strip().split(',')
                remove_machines(args)
            elif 'is_machine_alive' in inpstring:
                args = inpstring.split('is_machine_alive')[1].strip().split(',')
                print str(is_alive(args[0]))
            elif 'num_machines_alive' in inpstring:
                print N_ALIVEMACHINES
            else:
                print "ERROR: Command not found %s"%inpstring 
                print """ Supported Commands:
1. add_machines 3,5,7,10
2. remove_machines 1,2
3. is_machine_alive 5
4. num_machines_alive
""" 
                pass
        except Exception, e:
            print str(e)
            print "Try again"
              

 
def main():
    """ main function """
    get_input()

threadLock = threading.Lock()

if __name__ == "__main__":
    main()
