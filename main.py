from time import sleep
from threading import Thread
from modules import listener, subscriber


if __name__ == "__main__":
    print("* Starting listener...")
    Thread(target=listener.run_server).start()

    while True:
        # Possibly don't need to renew subscriptions - hub sends renew requests
        # print("* Renewing subscriptions...")
        # subscriber.subscribe_all()
        sleep(86400)
