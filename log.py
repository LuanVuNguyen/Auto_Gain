import datetime
import os
from control import TMPSTORE

def LOGGER(f,message):
    if not os.path.exists(TMPSTORE.outlog):
        os.mkdir(TMPSTORE.outlog)
    f = os.path.join(TMPSTORE.outlog,f)
    with open(f,mode='a') as f:
        f.write(str(message)+'\t'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        f.write('\n')
    f.close()
        
        