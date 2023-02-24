#!/home/mdi0316/anaconda3/bin/python
import inner
import sys

a = sys.argv[1]
b = sys.argv[2]

def service_func():
    print( 'service func' )

if __name__ == '__main__':
    # service.py executed as script
    # do something
    service_func()
    inner.some_func(a, b)
