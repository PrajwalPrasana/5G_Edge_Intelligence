import time
import torch
import numpy as np
import matplotlib.pyplot as plt
import random  # Chaos Engine!
import data_prep
import AImodel

print("\n INITIATING CONTINUOUS 5G THREAT MONITORING \n")

# 1. Load the Pre-Trained Brain
print("[System] Loading trained weights into Neural Network...")
input_features = data_prep.df_final.shape[1]
model = AImodel.AnomalyDetector(input_features)
model.load_state_dict(torch.load('5g_autoencoder.pth', weights_only=True))
model.eval() 

THRESHOLD = 0.05 
feature_names = data_prep.df_final.columns

# 2. Use the ENTIRE dataset this time
live_stream_data = data_prep.df_final.values

print("[System] Tapping into Endless 5G Edge Network stream...\n")
time.sleep(2)

# Loop through the entire dataset row by row
for i, packet in enumerate(live_stream_data):
    
    # Create a safe copy of the packet so we don't permanently ruin our dataset
    current_packet = packet.copy()
    
    # THE CHAOS ENGINE 
    # There is a 3% chance that any given packet will be a sudden Cyberattack
    # We wait until after flow 10 so your guide sees "Normal" traffic first
    if random.random() < 0.03 and i > 10:
        current_packet = current_packet * 50  # Poison the packet!
        
    # Convert and pass through the AI
    packet_tensor = torch.FloatTensor(current_packet).unsqueeze(0)
    reconstructed_packet = model(packet_tensor)
    loss = torch.nn.functional.mse_loss(reconstructed_packet, packet_tensor).item()
    
    # --- NORMAL TRAFFIC ---
    if loss < THRESHOLD:
        print(f"[Live] Flow ID {8800 + i}: NORMAL Traffic | Error: {loss:.5f}")
        time.sleep(0.3) # Fast stream for the demo
        
    # --- ANOMALY DETECTED! ---
    else:
        print(f"\n [CRITICAL ALERT] Flow ID {8800 + i}: ANOMALY DETECTED! ")
        print(f" Error Spike: {loss:.5f} (Exceeds {THRESHOLD} limit!)")
        print(">> Network halted. Generating XAI Feature Explanation Graph...\n")
        
        # Calculate XAI variables
        packet_np = packet_tensor.detach().numpy()[0]
        reconstructed_np = reconstructed_packet.detach().numpy()[0]
        feature_errors = np.abs(packet_np - reconstructed_np)
        
        plt.figure(figsize=(12, 7)) # Made it slightly bigger to fit text
        top_indices = np.argsort(feature_errors)[-10:] 
        
        # 1. THE AI TRANSLATION DICTIONARY
        # This translates the math into M.Tech thesis English
        feature_dictionary = {
            'Proto': 'Network Protocol (Attacker is likely spoofing TCP/UDP headers)',
            'sMeanPktSz': 'Source Mean Packet Size (Massive spike indicates a Volumetric DDoS Flood)',
            'sDSb': 'Differentiated Services Byte (Attacker is manipulating router QoS flags)',
            'sTtl': 'Time-to-Live (Unnatural packet lifespan, indicating spoofed origin)',
            'sHops': 'Network Hops (Packet is bouncing through unnatural routing paths)',
            'SrcTCPBase': 'Source TCP Base (TCP Handshake manipulation/SYN Flood)'
        }
        
        top_feature_name = feature_names[top_indices[-1]] # The #1 biggest error
        english_explanation = feature_dictionary.get(top_feature_name, 'Anomalous deviation in standard routing metrics.')

        plt.barh([feature_names[idx] for idx in top_indices], feature_errors[top_indices], color='crimson')
        plt.title(f"XAI Root Cause Analysis (Flow {8800 + i})", fontsize=16, fontweight='bold')
        plt.xlabel("Reconstruction Error (Deviation from Normal Baseline)", fontsize=12)
        
        # 2. ADD THE PLAIN ENGLISH REPORT TO THE GRAPH
        report_text = f"AI DIAGNOSIS REPORT \nPrimary Threat Vector: {top_feature_name}\nExplanation: {english_explanation}"
        
        # This prints a text box directly onto the bottom of your Matplotlib window
        plt.figtext(0.15, 0.02, report_text, fontsize=12, color='white', 
                    bbox=dict(facecolor='darkred', alpha=0.8, pad=10))

        plt.subplots_adjust(bottom=0.2) # Make room at the bottom for the text box
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.show()
        
        # When you close the graph window, the script resumes here:
        print("\n[System] Threat Isolated. Resuming normal network monitoring...\n")
        time.sleep(1.5)

print("\n=== SYSTEM SHUTDOWN ===")