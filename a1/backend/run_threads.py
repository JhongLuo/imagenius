import memcache as memcache
import app
import threading
import time

def run_memcache():
    memcache.webapp.run(host='0.0.0.0', port=5001, debug=False)
    
def run_api():
    app.webapp.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':

    # Executing the Threads seperatly.
    t1 = threading.Thread(target=run_memcache)
    t2 = threading.Thread(target=run_api)
    t1.start()
    time.spleep(3)
    t2.start()
