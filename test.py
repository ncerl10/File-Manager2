import os
import random
import time
def createFolder(name): # Helper function to create a new folder
    os.mkdir(f'test/{name}')

def createFile(path, size, name=f'RAND{str(random.randint(0, 10000000))}', ext="txt"): # Create a new file with a certain size in kilobytes
    with open(path + "/" + 'RAND' + str(random.randint(0, 10000000)) + "." + ext, "w") as f:
        f.write("A" * size * 1000)

def createFileWithTime(path, size=1,name=f'RAND{str(random.randint(0, 10000000))}', atime=None, mtime=None, ext="txt"): # Create file with specifed access time (atime) or modifed time (mtime)
    name = f'RAND{str(random.randint(0, 10000000))}' 
    with open(path + "/" + name + "." + ext, "w") as f:
        f.write("A" * size * 1000)
    a, m = os.stat(path + "/" + name + "." + ext).st_atime, os.stat(path + "/" + name + "." + ext).st_mtime
    if atime and mtime:
        os.utime(path + "/" + name + "." + ext, (atime, mtime)) # Change access time and modified time
    if atime:
        os.utime(path + "/" + name + "." + ext, (atime, m)) # Change only access time
    if mtime:
        os.utime(path + "/" + name + "." + ext, (a, mtime)) # Change only modified time

def createFileWithExt(path, size=1, ext="txt",name=f'RAND{str(random.randint(0, 10000000))}' ): # Creates a file with default size 1kb, and with a specified extension
    with open(path + "/" + f'RAND{str(random.randint(0, 10000000))}' + "." + ext, "w") as f:
        f.write("A" * size * 1000)

def randomCreate(path): # The function to randomly create files by size, time, or extension
    e = random.randint(0, 3)
    if e == 0:
        createFile(path, random.randint(1, 10))
    elif e == 1:
        createFileWithTime(path, size=random.randint(1, 10), atime=int(time.time()) - random.randint(100000, 100000000), mtime=int(time.time()) - random.randint(100000, 100000000))
    else:
        createFileWithExt(path, size=random.randint(1, 10), ext=random.choice(["txt", 'jpg', 'png', 'mp4', 'm4a']))

def massCreate(testcase, amount=100, atimes=False, mtimes=False, size=False, ext=False): # Function to mass create files randomly
    createFolder(testcase)
    for i in range(amount):
        randomCreate("test/" + testcase)
no = int(input("Enter the amount of files to create: "))
massCreate("test"+str(random.randint(1, 5000)), amount=no) # Mass creates 100 files, inside a folder

