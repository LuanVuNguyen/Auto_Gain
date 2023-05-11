import os
from datetime import datetime, timedelta
from control import CLEANJOB,TMPSTORE
from log import LOGGER
def delete_old_files():
    try:
        now = datetime.now().timestamp()
        for file_name in os.listdir(TMPSTORE.outlog):
            file_path = os.path.join(TMPSTORE.outlog, file_name)
            if os.path.isfile(file_path):
                created_time = os.path.getmtime(file_path)
                print(created_time)
                if now - created_time > CLEANJOB.older_file:
                    os.remove(file_path)     
    except Exception as e:
        LOGGER('exception','clean file: {}'.format(e))

    