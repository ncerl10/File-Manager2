import os
import random
import time
def createFolder(name):
    os.mkdir(f'test/{name}')

def createFile(path, size, name=f'RAND{str(random.randint(0, 10000000))}', ext="txt"): # In kb
    print(path + "/" + name + "." + ext)
    with open(path + "/" + 'RAND' + str(random.randint(0, 10000000)) + "." + ext, "w") as f:
        f.write("A" * size * 1000)

def createFileWithTime(path, size=1,name=f'RAND{str(random.randint(0, 10000000))}', atime=None, mtime=None, ext="txt"):
    name = f'RAND{str(random.randint(0, 10000000))}' 
    with open(path + "/" + name + "." + ext, "w") as f:
        f.write("A" * size * 1000)
    a, m = os.stat(path + "/" + name + "." + ext).st_atime, os.stat(path + "/" + name + "." + ext).st_mtime
    if atime and mtime:
        os.utime(path + "/" + name + "." + ext, (atime, mtime))
    if atime:
        os.utime(path + "/" + name + "." + ext, (atime, m))
    if mtime:
        os.utime(path + "/" + name + "." + ext, (a, mtime))

def createFileWithExt(path, size=1, ext="txt",name=f'RAND{str(random.randint(0, 10000000))}' ):
    with open(path + "/" + f'RAND{str(random.randint(0, 10000000))}' + "." + ext, "w") as f:
        f.write("A" * size * 1000)

def randomCreate(path):
    e = random.randint(0, 3)
    if e == 0:
        createFile(path, random.randint(1, 10))
    elif e == 1:
        createFileWithTime(path, size=random.randint(1, 10), atime=int(time.time()) - random.randint(10000, 1000000), mtime=int(time.time()) - random.randint(10000, 1000000))
    else:
        createFileWithExt(path, size=random.randint(1, 10), ext=random.choice(["txt", 'jpg', 'png', 'mp4', 'm4a']))

def massCreate(testcase, amount=100, atimes=False, mtimes=False, size=False, ext=False):
    createFolder(testcase)
    for i in range(amount):
        randomCreate("test/" + testcase)

massCreate("test"+str(random.randint(1, 6969)), amount=100)

