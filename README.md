# 5G_Edge_Intelligence# 5G Edge Intelligence: Unsupervised Anomaly Detection & XAI

## Project Overview
This repository contains a PyTorch-based framework for detecting cyberattacks in 5G Edge networks. Instead of relying on signature-based black-box models, this project uses an Unsupervised Deep Autoencoder to learn the baseline of normal 5G traffic. It features a real-time Explainable AI (XAI) dashboard to isolate and explain network threats (like DDoS or Spoofing) in plain English.

## Architecture

data_prep.py: Ingests network flow data, drops "cheating" labels for true unsupervised learning, and normalizes telemetry using MinMaxScaler.

train.py: Trains the PyTorch Autoencoder to reconstruct normal 5G traffic.

live_detect.py: An inference engine that simulates live edge network traffic. It catches anomalies via MSE loss spikes and triggers a Matplotlib XAI diagnostic dashboard.

live_packet_sniffer.py: A scapy-based network tap that captures real-world TCP/UDP packets from the local network interface to prove hardware integration capabilities.

## Prerequisites

Python 3.10+

Windows Administrator Privileges (Required for live_packet_sniffer.py)

##  Installation
Clone the repository and install the required dependencies:
git clone https://github.com/PrajwalPrasana/5G_Edge_Intelligence.git
cd 5G_Edge_Intelligence
pip install torch pandas numpy scikit-learn matplotlib scapy

##  How to Run the Project

Step 1: Train the AI Brain
Run the training script to generate the .pth weights file.
python train.py

Step 2: Start the Live Inference Engine
Run the live simulator. It will stream normal traffic and randomly inject a poison packet (Chaos Engine) to trigger the XAI dashboard.
python live_detect.py

Step 3: Capture Real Network Traffic (Proof of Concept)
Open your terminal as an Administrator, navigate to the project folder, and run:
python live_packet_sniffer.py

## XAI Dashboard Output
When an anomaly is detected, the system pauses and outputs a SHAP-style Bar Chart detailing the Exact Root Cause. For example: if an attacker attempts a volumetric flood, the system will isolate the sMeanPktSz (Source Mean Packet Size) as the compromised feature and alert the administrator.

