from utils.cloudwatch import Watcher
from utils.rds import StatsNames
from utils.cachering import CacheRing, key2hash
import datetime
import time

def watcher_test():
    begin = datetime.datetime.utcnow()
    while True:
        time.sleep(1)
        if datetime.datetime.utcnow() - begin > datetime.timedelta(seconds=70):
            break
        watcher = Watcher()
        for i in range(10):
            watcher.put_metric(StatsNames.total_requests, i)
        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=1)
        print(watcher.get_metric(StatsNames.total_requests, start, end))

def ring_test():
    ring = CacheRing()
    print([hex(v) for v in ring.boundaries])
    for _ in range(7):
        print("\nadd")
        ins = ring.add()
        for i in ins:
            print(i) 
        print(ring.cache_num)
        print(ring.get_partitions())
    for _ in range(7):
        print("\nremove")
        ins = ring.remove()
        for i in ins:
            print(i)
        print(ring.cache_num)
        print(ring.get_partitions())

def hash_test():
    ring = CacheRing()
    hash_list = []
    for i in range(10):
        hash_list.append(key2hash(str(i)))
    print(hash_list)
    print([hex(v) for v in hash_list])
    partition_count = [0] * ring.partition_num
    right_count = 0
    for i in range(10000):
        hash = key2hash(str(i))
        partition = ring.hash2partition(hash)
        partition_count[partition] += 1
        right_count += (hash >= ring.boundaries[partition] and hash < ring.boundaries[partition + 1])
    print(right_count / 10000) # should be 1.0
    print(partition_count) # should be evenly distributed

def sched_test():
    import sched, time
    s = sched.scheduler(time.time, time.sleep)
    def print_time(a='default'):
        print("From print_time", time.time(), a)

    def print_some_times():
        print(time.time())
        s.enter(10, 1, print_time)
        s.enter(5, 2, print_time, argument=('positional',))
        # despite having higher priority, 'keyword' runs after 'positional' as enter() is relative
        s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
        s.enterabs(1_650_000_000, 10, print_time, argument=("first enterabs",))
        s.enterabs(1_650_000_000, 5, print_time, argument=("second enterabs",))
        s.run()
        print(time.time())
    print_some_times()
    for i in range(10):
        print(i)
          
def apscheduler_test():
    from apscheduler.schedulers.background import BackgroundScheduler
    lis = []
    def start_scheduler(lis):
        def run(lis):
            while True:
                time.sleep(1)
                lis.append('in scheduler')
                print(lis)
        scheduler = BackgroundScheduler()
        # just run once will do
        scheduler.add_job(func=run, args=(lis,))
        scheduler.start()
    start_scheduler(lis)
    time.sleep(3)
    for i in range(10):
        print(lis)
        lis.append(f'in main {i}')
        time.sleep(1)
    
def rds_test():
    from utils.rds import get_keys, set_key, delete_keys, key2path, reset_stats
    from utils.rds import init_database, get_memcache_status, set_memcache_status, reset_memcache_status
    def images_test() :
        print(get_keys()) # []
        for i in range(100):
            set_key(f"{i}", f"{i}.jpg")
        print(get_keys())
        print([key2path(x) for x in get_keys()])
        print([key2path(x) for x in range(100, 110)])
        delete_keys()
        print(get_keys()) # []

    def stats_test():
        reset_stats()
        # print(get_stat(StatsNames.max_size))
        # print(get_stat(StatsNames.replacement_policy))
        # set_stat(StatsNames.max_size, 100)
        # set_stat(StatsNames.replacement_policy, ReplacementPolicies.RANDOM.value)
        # print(get_stat(StatsNames.max_size))
        # print(get_stat(StatsNames.replacement_policy))
        # set_stat(StatsNames.max_size, 10000)
        # set_stat(StatsNames.replacement_policy, ReplacementPolicies.LRU.value)
        # print(get_stat(StatsNames.max_size))
        # print(get_stat(StatsNames.replacement_policy))
        
        # print(get_stat(StatsNames.total_requests))
        # print(get_stat(StatsNames.read_requests))
        # print(get_stat(StatsNames.missed_requests))
        # add_stat(StatsNames.total_requests, 100)
        # add_stat(StatsNames.read_requests, 200)
        # add_stat(StatsNames.missed_requests, 300)
        # print(get_stat(StatsNames.total_requests))
        # print(get_stat(StatsNames.read_requests))
        # print(get_stat(StatsNames.missed_requests))

    def memcache_status_test():
        init_database()
        for i in range(8):
            print(get_memcache_status(i))
        for i in range(3):
            set_memcache_status(i * 2, True)
        for i in range(8):
            print(get_memcache_status(i))
        reset_memcache_status()
        for i in range(8):
            print(get_memcache_status(i))
    
    memcache_status_test()
           
        
if __name__ == "__main__":
    # watcher_test()
    # ring_test()
    # hash_test()
    # sched_test()
    # apscheduler_test()
    # rds_test()
    pass