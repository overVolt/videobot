from time import sleep
from threading import Thread
from modules import listener
from modules import subscriber


if __name__ == "__main__":
    print("* Starting listener...")
    Thread(target=listener.run_server).start()

    while True:
        print("* Renewing subscriptions...")
        subscriber.subscribe_all()
        sleep(86400)
