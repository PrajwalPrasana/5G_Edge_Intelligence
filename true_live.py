from scapy.all import sniff, IP, TCP, UDP, conf
import torch
import numpy as np
import joblib
import warnings
import AImodel
import data_prep

warnings.filterwarnings("ignore", category=UserWarning)

print("\n🚨 INITIATING TRUE LIVE EDGE AI INFERENCE 🚨\n")

# 1. Load Brain, Scaler, and Feature Map
print("[System] Loading Autoencoder and MinMaxScaler...")
feature_names = list(data_prep.df_final.columns) # Get the exact final columns
input_features = len(feature_names)

model = AImodel.AnomalyDetector(input_features)
model.load_state_dict(torch.load('5g_autoencoder.pth', weights_only=True))
model.eval()

scaler = joblib.load('5g_scaler.save')
THRESHOLD = 0.05

active_interface = conf.route.route("8.8.8.8")[0]
print(f"[System] Auto-detected active network card: {active_interface}")
print("[System] Live AI Analysis started. Press Ctrl+C to stop.\n")

def process_live_packet(packet):
    try:
        if IP in packet:
            # 2. Extract Valid Flow-Matching Features from Scapy
            packet_size = len(packet)
            ttl = packet[IP].ttl
            
            tcp_window = 0
            is_tcp = 0
            is_udp = 0
            
            if TCP in packet: 
                is_tcp = 1
                tcp_window = packet[TCP].window
            elif UDP in packet: 
                is_udp = 1

            # 3. Dynamically Map to the AI's Exact Receptors
            live_features = np.zeros(shape=(1, input_features))
            
            # Helper function to safely inject data if the column exists
            def inject_feature(col_name, value):
                if col_name in feature_names:
                    live_features[0][feature_names.index(col_name)] = value

            # Mapping Scapy packet data to your specific dataset columns
            inject_feature('sTtl', ttl)
            inject_feature('TotBytes', packet_size)
            inject_feature('SrcBytes', packet_size)
            inject_feature('sMeanPktSz', packet_size)
            inject_feature('TotPkts', 1)
            inject_feature('SrcPkts', 1)
            inject_feature('SrcWin', tcp_window)
            
            # Handling Protocol if it was One-Hot Encoded in data_prep.py
            inject_feature('Proto_tcp', is_tcp)
            inject_feature('Proto_udp', is_udp)
            
            # 4. Scale and Predict
            scaled_live_features = scaler.transform(live_features)
            packet_tensor = torch.FloatTensor(scaled_live_features)
            
            reconstructed = model(packet_tensor)
            loss = torch.nn.functional.mse_loss(reconstructed, packet_tensor).item()
            
            # 5. The Verdict & Real-Time XAI
            if loss < THRESHOLD:
                pass # Only print anomalies to keep the terminal clean
            else:
                original_np = scaled_live_features[0]
                reconstructed_np = reconstructed.detach().numpy()[0]
                feature_errors = np.abs(original_np - reconstructed_np)
                
                top_error_index = np.argmax(feature_errors)
                top_culprit = feature_names[top_error_index]
                
                print(f"🚨 [CRITICAL] ANOMALY DETECTED! Error: {loss:.5f} 🚨")
                print(f"   => XAI DIAGNOSIS: Root cause feature is [{top_culprit}]\n")
                
    except Exception as e:
        pass 

sniff(iface=active_interface, prn=process_live_packet, store=False)