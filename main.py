from worker.handle_data import Datahandler_worker
from worker.recording import recording_worker
import threading


p1 = threading.Thread(target=recording_worker)
p2 = threading.Thread(target=Datahandler_worker)


p1.start()
p2.start()

