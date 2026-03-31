from scapy.all import *
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('packet_sniffer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedPacketSniffer:
    def __init__(self):
        self.packet_count = 0
        self.protocol_stats = {
            'TCP': 0,
            'UDP': 0,
            'ICMP': 0,
            'ARP': 0,
            'Other': 0
        }

    def packet_callback(self, packet):
        try:
            self.packet_count += 1

            # Extract IP information if present
            ip_layer = packet.getlayer(IP)
            if ip_layer is not None:
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
            else:
                src_ip = "N/A"
                dst_ip = "N/A"

            # Determine the protocol
            if TCP in packet:
                protocol = 'TCP'
                self.protocol_stats['TCP'] += 1
                tcp_layer = packet.getlayer(TCP)
                src_port = tcp_layer.sport
                dst_port = tcp_layer.dport
            elif UDP in packet:
                protocol = 'UDP'
                self.protocol_stats['UDP'] += 1
                udp_layer = packet.getlayer(UDP)
                src_port = udp_layer.sport
                dst_port = udp_layer.dport
            elif ICMP in packet:
                protocol = 'ICMP'
                self.protocol_stats['ICMP'] += 1
                src_port = "N/A"
                dst_port = "N/A"
            elif ARP in packet:
                protocol = 'ARP'
                self.protocol_stats['ARP'] += 1
                src_port = "N/A"
                dst_port = "N/A"
            else:
                protocol = 'Unknown'
                self.protocol_stats['Other'] += 1
                src_port = "N/A"
                dst_port = "N/A"

            # Extract additional packet details
            packet_length = len(packet)
            packet_hex = bytes(packet).hex()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Log the packet details
            logger.info(
                f"Pkt #{self.packet_count} ({timestamp}):\n"
                f"Source: {src_ip}:{src_port}\n"
                f"Destination: {dst_ip}:{dst_port}\n"
                f"Protocol: {protocol}\n"
                f"Length: {packet_length} bytes\n"
                f"Packet Type: {type(packet).__name__}\n"
                f"Hex: {packet_hex[:50]}...\n"
                f"---\n"
            )

        except Exception as e:
            logger.error(f"Error processing packet: {str(e)}")

    def display_stats(self):
        logger.info("\nCapture Statistics:")
        logger.info("--------------------")
        for proto, count in self.protocol_stats.items():
            logger.info(f"{proto}: {count} packets")

def main():
    sniffer = EnhancedPacketSniffer()

    # Interactive filter selection
    print("Select a filter type:")
    print("1. TCP only")
    print("2. UDP only")
    print("3. ICMP only")
    print("4. Custom BPF filter")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        filter_expr = 'tcp'
    elif choice == '2':
        filter_expr = 'udp'
    elif choice == '3':
        filter_expr = 'icmp'
    elif choice == '4':
        filter_expr = input("Enter your custom BPF filter: ")
    else:
        logger.error("Invalid choice. Defaulting to TCP.")
        filter_expr = 'tcp'

    if os.geteuid() != 0:
        logger.error("Please run as root!")
        return

    try:
        logger.info(f"Starting packet sniffer with filter '{filter_expr}'...")
        sniff(prn=sniffer.packet_callback, store=False, filter=filter_expr)
    except KeyboardInterrupt:
        sniffer.display_stats()
        logger.info("\nStopping packet sniffer. Goodbye!")

if __name__ == "__main__":
    main()