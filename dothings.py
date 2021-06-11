#!/usr/bin/python3

import os, threading, time

def runcrypto():
    # run an openssl speed test - alter the algo to be something hopefully common across platforms
    # you can also do hashing here - ie: sha256 
    return(os.system('openssl speed aes-256-cbc 2>&1 | > /dev/null' ))

def runcompres():
    # just compress some largeish ( ~3 GB ) file
    return(os.system('gzip -c vmcore-bz1785392-3 > /dev/null'))

def runnetget():
    # pull some large file out of a web server - again ~3 GB seems useful for this type of test
    return(os.system('wget -q http://10.0.0.1/install_server/ovas/appliance.ova -O /dev/null'))

def rundiskio():
    # bonnie can do lots of things - here we tell it not to bother with the large file creation ( -s 0 )
    #   and for the random file work create 2048 ( 2 * 1024 ) files, of sizes from 512 bytes down to 2 bytes, across 64 directories
    return(os.system('bonnie++ -q -c 4 -d ./mnt -s 0 -n 2:512:4:64 2>&1 |  > /dev/null'))

class AsyncRunner(threading.Thread):
    def __init__(self, runthis, runduration):
        threading.Thread.__init__(self)
        self.runthis = runthis
        self.runduration = runduration

    def run(self):
        counter = 0 
        starttime = time.time()
        curtime = time.time()
        print('Starting ', self.runthis, ' at ', starttime ) 
        while (starttime + self.runduration > curtime):    
            counter = counter + 1
            print('started ', self.runthis, ' at ', starttime )
            print('running ', self.runthis, ' till ', starttime + self.runduration )
            rc = self.runthis()
            print('ran ', self.runthis, ' had ' ,starttime + self.runduration - curtime, 'to go and ran ', counter, 'so far')
            curtime = time.time()

        print('Finished run of ', self.runthis, ' at ', curtime, ' and ran it ', counter, ' times'  ) 
        return()

print("startin")

# call one of our functions in a thread, and run it for 60 seconds. 
compproc = AsyncRunner(runcompres, 60)
compproc.start()

crypproc = AsyncRunner(runcrypto, 60)
crypproc.start()

netgproc = AsyncRunner(runnetget, 60)
netgproc.start()

diskproc = AsyncRunner(rundiskio, 60)
diskproc.start()
diskproc = AsyncRunner(rundiskio, 60)
diskproc.start()
diskproc = AsyncRunner(rundiskio, 60)
diskproc.start()
diskproc = AsyncRunner(rundiskio, 60)
diskproc.start()





exit(0)
