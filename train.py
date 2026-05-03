import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

print("\n=== STAGE 3: AI MODEL TRAINING ===")

# 1. Import your custom files! 
# When we import data_prep, it automatically runs your cleaning script first.
import data_prep  
import AImodel    

# Grab the clean, scaled data table
df = data_prep.df_final

# 2. Convert Data to Tensors
print("\n[1/3] Converting data for PyTorch...")
# PyTorch cannot read Pandas tables. We must convert the data into "Tensors" (PyTorch's matrix format)
data_tensor = torch.FloatTensor(df.values)

# We feed data to the AI in small chunks (batches of 64) so it doesn't crash your computer's memory
dataset = TensorDataset(data_tensor, data_tensor) # Autoencoders map input to input!
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# 3. Initialize the Brain
print("[2/3] Initializing the Autoencoder...")
input_features = df.shape[1] # Automatically counts your 50+ columns
model = AImodel.AnomalyDetector(input_features)

# The Optimizer (Adam) is the algorithm that tweaks the math to make the AI smarter
optimizer = optim.Adam(model.parameters(), lr=0.001)
# The Loss Function (MSE) calculates exactly how badly the AI failed to reconstruct the data
criterion = nn.MSELoss()

# 4. The Training Loop
epochs = 5 # How many times the AI will read the entire dataset
print(f"\n[3/3] Starting Training for {epochs} Epochs...\n")

for epoch in range(epochs):
    total_loss = 0
    
    # Loop through every batch of 64 rows
    for batch_data, _ in dataloader:
        
        # Step A: Reset the math
        optimizer.zero_grad()
        
        # Step B: Feed the data in (Compress and Decompress)
        reconstructed = model(batch_data)
        
        # Step C: Calculate the Reconstruction Error
        loss = criterion(reconstructed, batch_data)
        
        # Step D: Update the AI's internal weights to do better next time
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        
    # Calculate the average error for this epoch
    avg_loss = total_loss / len(dataloader)
    print(f"   -> Epoch [{epoch+1}/{epochs}] | Reconstruction Error: {avg_loss:.5f}")

print("\n=== TRAINING COMPLETE ===")

# 5. Save the trained brain!
torch.save(model.state_dict(), '5g_autoencoder.pth')
print(" Model weights saved successfully as '5g_autoencoder.pth'")
print("The AI is now fully trained and ready for Anomaly Detection!")