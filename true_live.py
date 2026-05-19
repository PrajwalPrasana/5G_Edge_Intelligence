from scapy.all import sniff, IP, TCP, UDP, conf
import torch
import numpy as np
import joblib
import AImodel
import data_prep

import warnings
# Mute the sklearn feature name warning for a clean terminal output
warnings.filterwarnings("ignore", category=UserWarning)

print("\n INITIATING TRUE LIVE EDGE AI INFERENCE \n")

# 1. Load the AI Brain and the Scaler
print("[System] Loading Autoencoder and MinMaxScaler...")
input_features = data_prep.df_final.shape[1]
model = AImodel.AnomalyDetector(input_features)
model.load_state_dict(torch.load('5g_autoencoder.pth', weights_only=True))
model.eval()

scaler = joblib.load('5g_scaler.save')
THRESHOLD = 0.05

# 2. Dynamically Find the Network Door
active_interface = conf.route.route("8.8.8.8")[0]
print(f"[System] Auto-detected active network card: {active_interface}")
print("[System] Live AI Analysis started. Press Ctrl+C to stop.\n")

def process_live_packet(packet):
    try:
        if IP in packet:
            # --- EXTRACTING 10+ FEATURES VIA SCAPY ---
            packet_size = len(packet)
            ttl = packet[IP].ttl
            ip_ihl = packet[IP].ihl
            ip_flags = int(packet[IP].flags)
            
            protocol_num = 0 
            src_port = 0
            dst_port = 0
            tcp_window = 0
            tcp_flags = 0
            data_offset = 0

            if TCP in packet: 
                protocol_num = 1
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                tcp_window = packet[TCP].window
                tcp_flags = int(packet[TCP].flags)
                data_offset = packet[TCP].dataofs
            elif UDP in packet: 
                protocol_num = 2
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport

            # Format it for the AI (Injecting our 10 features)
            live_features = np.zeros(shape=(1, input_features))
            live_features[0][0] = protocol_num
            live_features[0][1] = packet_size
            live_features[0][2] = ttl
            live_features[0][3] = ip_ihl
            live_features[0][4] = ip_flags
            live_features[0][5] = src_port
            live_features[0][6] = dst_port
            live_features[0][7] = tcp_window
            live_features[0][8] = tcp_flags
            live_features[0][9] = data_offset
            
            # Scale and Predict
            scaled_live_features = scaler.transform(live_features)
            packet_tensor = torch.FloatTensor(scaled_live_features)
            
            reconstructed = model(packet_tensor)
            loss = torch.nn.functional.mse_loss(reconstructed, packet_tensor).item()
            
            # Real-Time XAI
            if loss < THRESHOLD:
                print(f"[LIVE] Packet {packet_size}b | Proto: {protocol_num} | Status: NORMAL | Error: {loss:.5f}")
            else:
                original_np = scaled_live_features[0]
                reconstructed_np = reconstructed.detach().numpy()[0]
                feature_errors = np.abs(original_np - reconstructed_np)
                
                top_error_index = np.argmax(feature_errors)
                feature_names = data_prep.df_final.columns
                top_culprit = feature_names[top_error_index]
                
                print(f"🚨 [CRITICAL] ANOMALY DETECTED! Error: {loss:.5f} 🚨")
                print(f"   => XAI DIAGNOSIS: Root cause feature is [{top_culprit}]\n")
                
    except Exception as e:
        pass

# Start Sniffing & Inferencing!
sniff(iface=active_interface, prn=process_live_packet, store=False)