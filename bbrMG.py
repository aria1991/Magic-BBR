# Constants
INITIAL_CWND = 10
MIN_CWND = 2
MAX_CWND = 1000000
MIN_RTT_SAMPLES = 8  # Number of RTT samples needed for min RTT to stabilize
BBR_GAIN = 2.7  # Gain for BBR congestion control equation

# Variables
cwnd = INITIAL_CWND  # Congestion window
ssthresh = float("inf")  # Slow start threshold
in_slow_start = True  # Flag for slow start phase
min_rtt = float("inf")  # Minimum RTT
rtt_samples = []  # List of recent RTT samples

while True:
  # Send packets up to the current congestion window size
  send_packets(cwnd)

  # Wait for ACKs for the sent packets
  rtt, acked_packets = wait_for_acks()

  # Update the list of recent RTT samples
  rtt_samples.append(rtt)
  if len(rtt_samples) > MIN_RTT_SAMPLES:
    rtt_samples.pop(0)

  # Calculate the minimum RTT from the recent samples
  min_rtt = min(rtt_samples)

  # Check if we are in the slow start phase
  if in_slow_start:
    # Increase the congestion window by the number of ACKed packets
    cwnd += acked_packets

    # If the congestion window exceeds the slow start threshold,
    # enter the congestion avoidance phase
    if cwnd > ssthresh:
      in_slow_start = False
  else:
    # In congestion avoidance phase

    # Calculate the "bottleneck bandwidth", which is the number of
    # ACKed bytes per RTT
    bw = acked_bytes / rtt

    # Calculate the new congestion window size based on the
    # bottleneck bandwidth and the minimum RTT
    cwnd = bw * min_rtt * BBR_GAIN

  # Check if the connection is experiencing packet loss
  if acked_packets < cwnd:
    # Set the slow start threshold to half of the current congestion window
    ssthresh = cwnd / 2
    # Reset the congestion window to the slow start threshold
    cwnd = ssthresh
    # Enter the slow start phase
    in_slow_start = True

  # Ensure that the congestion window stays within the min and max limits
  cwnd = max(MIN_CWND, min(cwnd, MAX_CWND))
