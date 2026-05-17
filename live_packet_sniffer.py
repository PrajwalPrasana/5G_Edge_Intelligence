from scapy.all import sniff, IP, TCP, UDP
import datetime

print("\n INITIATING LIVE EDGE NETWORK INTERFACE TAP ")
print("[System] Binding to local network adapter...")
print("[System] Listening for live TCP/UDP traffic... Press Ctrl+C to stop.\n")

# This function runs every single time a real packet hits your computer
def process_packet(packet):
    try:
        # We only care about IP packets (Internet Protocol)
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            packet_size = len(packet)
            timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]

            # Check if it's TCP or UDP to simulate telecom tracking
            protocol = "UNKNOWN"
            if TCP in packet:
                protocol = "TCP"
            elif UDP in packet:
                protocol = "UDP"

            # Print the live traffic log
            print(f"[{timestamp}] FLOW RECV | Proto: {protocol} | Size: {packet_size} bytes | Path: {ip_src} -> {ip_dst}")
            
    except Exception as e:
        pass # Ignore weird background system packets

# Start sniffing! (store=False keeps it from crashing your RAM)
sniff(prn=process_packet, store=False)