from time import sleep
from threading import Thread
from modules import listener
from modules import subscriber


if __name__ == "__main__":
    Thread(target=listener.run_server).start()

    while True:
        subscriber.subscribe_all()
        sleep(86400)
