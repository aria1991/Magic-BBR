import argparse
import sys
import time

import psutil

from collections import deque

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, default=60,
                        help='duration of the test in seconds')
    parser.add_argument('--window', type=int, default=10,
                        help='size of the congestion window in segments')
    parser.add_argument('--bandwidth', type=int, default=1000000,
                        help='bandwidth of the bottleneck link in bps')
    parser.add_argument('--delay', type=int, default=100,
                        help='propagation delay of the bottleneck link in ms')
    parser.add_argument('--loss', type=float, default=0.0,
                        help='packet loss rate on the bottleneck link')
    parser.add_argument('--testbed', type=str, default='localhost',
                        help='name or IP address of the testbed host')
    return parser.parse_args()

def get_cpu_utilization():
    return psutil.cpu_percent()

def get_memory_utilization():
    return psutil.virtual_memory().percent

def get_network_utilization(interface):
    stats = psutil.net_io_counters(pernic=True)[interface]
    return stats.bytes_sent, stats.bytes_recv

def run_test(duration, window, bandwidth, delay, loss, testbed):
    send_times = deque()
    recv_times = deque()
    send_bytes = 0
    recv_bytes = 0
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        # Send a packet
        send_times.append(time.time())
        send_bytes += 1400
        # Receive an ACK
        recv_times.append(time.time())
        recv_bytes += 40
        # Update the congestion window size
        if len(send_times) > window:
            send_times.popleft()
            recv_times.popleft()
        # Simulate packet loss
        if loss > 0 and loss < 1:
            if random.random() < loss:
                send_times.popleft()
        # Simulate network delay
        time.sleep(delay / 1000)
    elapsed_time = time.time() - start_time
    return elapsed_time, send_bytes, recv_bytes

def main():
        args = parse_args()
    duration = args.duration
    window = args.window
    bandwidth = args.bandwidth
    delay = args.delay
    loss = args.loss
    testbed = args.testbed
    print('Running test with duration={}, window={}, bandwidth={}, delay={}, loss={}, testbed={}'.format(
        duration, window, bandwidth, delay, loss, testbed))
    elapsed_time, send_bytes, recv_bytes = run_test(duration, window, bandwidth, delay, loss, testbed)
    cpu_util = get_cpu_utilization()
    mem_util = get_memory_utilization()
    send_rate = send_bytes * 8 / elapsed_time / 1000000
    recv_rate = recv_bytes * 8 / elapsed_time / 1000000
    print('Elapsed time: {} seconds'.format(elapsed_time))
    print('CPU utilization: {}%'.format(cpu_util))
    print('Memory utilization: {}%'.format(mem_util))
    print('Send rate: {} Mbps'.format(send_rate))
    print('Receive rate: {} Mbps'.format(recv_rate))

if __name__ == '__main__':
    main()

