# Magic-BBR
A server-side implementation of the Magic BBR (Bottleneck Bandwidth and Round-trip propagation time) congestion control algorithm


## Theory
The Magic BBR congestion control algorithm is a variant of the Bottleneck Bandwidth and Round-trip propagation time (BBR) algorithm, which was developed by Google to improve the performance of TCP connections over high-bandwidth, long-latency networks
<!--more-->

- The main idea behind BBR is to estimate the bottleneck bandwidth and the minimum round-trip time (RTT) for a connection, and use these estimates to adjust the congestion window size in order to maximize throughput.

<!--more-->



- The congestion window size, `cwnd`, is a measure of how much data can be in transit at any given time. It is determined by the sender and controls how much data can be sent before receiving an acknowledgement (ACK) from the receiver.


<!--more-->


- The slow start threshold, `ssthresh`, is a congestion window size threshold that determines when the connection should transition from the slow start phase to the congestion avoidance phase.

<!--more-->

- In the slow start phase, the congestion window size is increased exponentially with each ACK received. This is intended to quickly ramp up the sending rate in order to discover the available bandwidth.

- In the congestion avoidance phase, the congestion window size is increased more slowly, based on the estimated bottleneck bandwidth and the minimum RTT. This helps to prevent the connection from overloading the network and causing packet loss.
<!--more-->


The algorithm for adjusting the congestion window size in the congestion avoidance phase is as follows:

<!--more-->

```
bw = acked_bytes / rtt  # Estimate the bottleneck bandwidth
cwnd = bw * min_rtt * BBR_GAIN  # Calculate the new congestion window size

```
The `bw` variable is the estimated bottleneck bandwidth, which is calculated by dividing the number of ACKed bytes by the RTT. The `min_rtt` variable is the minimum RTT for the connection, which is calculated from recent RTT samples. The `BBR_GAIN` constant is a gain factor that adjusts the congestion window size based on the desired level of congestion control.
<!--more-->


<!--more-->

If the connection experiences packet loss, the algorithm enters the slow start phase and the congestion window size is reset to the slow start threshold. The slow start threshold is then set to half of the current congestion window size in order to reduce the sending rate and prevent further packet loss.
<!--more-->



<!--more-->
In addition to estimating the bottleneck bandwidth and the minimum RTT, the BBR algorithm also tracks the "full pipe capacity", which is the maximum amount of data that can be sent over the connection without experiencing packet loss. This is calculated using the following formula:

```
full_pipe_capacity = bw * max_rtt

```
<!--more-->
Where `bw `is the estimated bottleneck bandwidth and `max_rtt` is the maximum RTT for the connection.

The full pipe capacity can be used to determine the optimal congestion window size for the connection. The BBR algorithm uses the following equation to calculate the congestion window size based on the full pipe capacity:

```
cwnd = BBR_GAIN * full_pipe_capacity

```
Where `BBR_GAIN` is a gain factor that adjusts the congestion window size based on the desired level of congestion control.

The BBR algorithm also includes a "drain" phase, which is used to drain the remaining data in the congestion window when the connection is closed or when the BBR algorithm is disabled. In the drain phase, the congestion window size is gradually reduced to the slow start threshold in order to avoid disrupting the network.

Fore more information check this **[Article](https://queue.acm.org/detail.cfm?id=3022184 "Article")**
<!--more-->


## About the code

The script provided in this repository uses a few helper functions, such as `send_packets()` and `wait_for_acks()`, which would need to be implemented as well.

 `send_packets()` should send a specified number of packets to the server, and `wait_for_acks()` should wait for acknowledgement (ACK) packets from the server and return the round-trip time (RTT) and the number of ACKed packets.

<!--more-->

#### Additionally

This script includes several enhancements comparing to other scripts :

- It introduces a new constant, `MIN_RTT_SAMPLES`, which is the number of RTT samples needed for the minimum RTT to stabilize.


- It introduces a new constant, `BBR_GAIN`, which is the gain factor used in the Magic BBR congestion control equation.


- It maintains a list of recent RTT samples and calculates the minimum RTT from those samples. This helps to ensure that the minimum RTT is accurate and up-to-date.


- It checks for packet loss

