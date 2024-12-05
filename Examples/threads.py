from time import sleep
from threading import Thread


def long_function():
    print('Starting...')
    sleep(5)
    print('Finishing...')


print('Before')
threads = [Thread(target=long_function) for i in range(100)]
for t in threads:
    t.start()
print('After')