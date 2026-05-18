from scapy.all import sniff, IP, TCP, UDP, conf
import datetime

print("\nINITIATING LIVE EDGE NETWORK INTERFACE TAP")

# --- NEW DYNAMIC DETECTION ---
# We ask the OS: "Which interface would you use to reach the open internet?"
active_interface = conf.route.route("8.8.8.8")[0]
print(f"[System] Auto-detected active network card: {active_interface}")
# -----------------------------

print("[System] Listening for live TCP/UDP traffic... Press Ctrl+C to stop.\n")

def process_packet(packet):
    try:
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            packet_size = len(packet)
            timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]

            protocol = "UNKNOWN"
            if TCP in packet: protocol = "TCP"
            elif UDP in packet: protocol = "UDP"

            print(f"[{timestamp}] FLOW RECV | Proto: {protocol} | Size: {packet_size} bytes | Path: {ip_src} -> {ip_dst}")
            
    except Exception as e:
        pass 

# Now we pass the dynamically detected interface!
sniff(iface=active_interface, prn=process_packet, store=False)