import os,time
from threading import Thread

startTime = time.time()


class CopyThread(Thread):
    def __init__(self,args,name=""):
        Thread.__init__(self)
        self.name=name
        self.args = args
    
    def run(self) :
        curdir = os.getcwd()
        originalFile = open(curdir+"/"+self.args[0],"rb") 
        destFile = open(curdir+"/"+self.args[1],"wb")
        
        thStartTime = time.time()
        thLogStartTime = thStartTime - startTime  
        
        log = open("log.txt","a")
        log.write("{:.2f} Start Copying {} to {} \n".format(thLogStartTime,self.args[0],self.args[1]))
        log.close()
        
        fsrc_read = originalFile.read
        fdst_write = destFile.write
        while True:
            buf = fsrc_read(self.args[2])
            if not buf :
                break
            fdst_write(buf)
        thEndTime = time.time()
        theLogEndTime = thEndTime - startTime
        log = open("log.txt","a")
        log.write("{:.2f} {} is copied completely  \n".format(theLogEndTime,self.args[1]))
        log.close()
        originalFile.close()
        destFile.close()

def process() :
    count = 0
    while True :
        count+=1
        fileName = input("input the file name : ")
        if fileName == "exit" :
            return
        destName = input("input the new name: ")
        copyThread = CopyThread(args=(fileName,destName,10*1024),name = count)
        copyThread.start()
          

if __name__ == "__main__" :
    process()






