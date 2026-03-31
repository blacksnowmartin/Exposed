from scapy.all import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

count = 0

def packet_callback(packet):
    global count
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = 'Unknown'
        if packet.proto == 6:  # TCP is 6
            protocol = 'TCP'
        elif packet.proto == 17:  # UDP is 17
            protocol = 'UDP'
        elif packet.proto == 1:  # ICMP is 1
            protocol = 'ICMP'
        else:
            protocol = f"Others ({packet.proto})"
        length = len(packet)
        count += 1
        logger.info(f"Pkt #{count}: {src_ip} -> {dst_ip}, Proto: {protocol}, Len: {length}")
    return

def main():
    if os.geteuid() != 0:
        logger.error("Please run as root!")
        return
    logger.info("Starting packet sniffer. Press Ctrl+C to stop.")
    try:
        sniff(prn=packet_callback, store=False)
    except KeyboardInterrupt:
        logger.info("\nStopping packet sniffer. Goodbye!")

if __name__ == "__main__":
    main()