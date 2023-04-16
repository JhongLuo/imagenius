import api
import matplotlib.pyplot as plt
import random
import time
from concurrent.futures import ThreadPoolExecutor


tags = api.get_tags()['tags']
tags = set(tags)
print(tags)
tags.remove('All')
print('len(tags)', len(tags))
tags = list(tags)


def tags_count2time(tags_count):
    selected_tags = random.sample(tags, tags_count)
    print('selected_tags', selected_tags)
    start = time.time()
    api.search_by_tags(selected_tags)
    return time.time() - start

def tags_count2avg_time(total_iter, tags_count):
    return sum(tags_count2time(tags_count) for _ in range(total_iter)) / total_iter

def get_latency(max_tags):
    latency = []
    for tags_count in range(1, max_tags):
        latency.append(tags_count2avg_time(15, tags_count))
    return latency

def get_latency_PNG():
    max_tags = 8
    plt.clf()
    plt.plot([i for i in range(1, max_tags)], get_latency(max_tags))
    plt.xlabel('Number of Tags')
    plt.ylabel('Average Latency (seconds)')
    plt.title('Retriving Images Latency vs Number of Tags')
    plt.grid()
    plt.savefig('Latency.png')


NUM_TESTS = 10
TEST_DURATION = 3
def performance_test(max_tags):
    def run_test(selected_tags):
        start_time = time.time()
        requests_count = 0

        while time.time() - start_time < TEST_DURATION:
            api.search_by_tags(selected_tags)
            requests_count += 1

        return requests_count

    tag_counts = list(range(1, max_tags))
    throughputs = []

    with ThreadPoolExecutor() as executor:
        for tag_count in tag_counts:
            total_requests_count = 0
            test_futures = []

            for _ in range(NUM_TESTS):
                time.sleep(0.01)
                selected_tags = random.sample(tags, tag_count)
                future = executor.submit(run_test, selected_tags)
                test_futures.append(future)

            for future in test_futures:
                total_requests_count += future.result()

            throughput = total_requests_count / (TEST_DURATION)
            throughputs.append(throughput)

    return tag_counts, throughputs


def get_throughput():
    api.change_provisioned_throughput(free_to_test=True)
    time.sleep(10)
    input('Press Enter to start performance test...')
    max_tags = 8
    tag_counts, throughputs = performance_test(max_tags)
    plt.clf()
    plt.plot(tag_counts, throughputs)
    plt.xlabel('Number of Tags')
    plt.ylabel('Throughput (requests per second)')
    plt.title('Retriving Images Throughput vs Number of Tags')
    plt.grid()
    plt.savefig('Throughput.png')
    api.change_provisioned_throughput(free_to_test=False)
    
get_throughput()