import torch
import torch.nn as nn

print("--- Initializing 5G Autoencoder ---")

#create a Neural Network class using PyTorch
class AnomalyDetector(nn.Module):
    def __init__(self, input_size):
        super(AnomalyDetector, self).__init__()
        
        # 1. THE ENCODER takes the input and shrinks it layer by layer
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(), # ReLU is the activation function that helps the AI learn complex patterns
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 8) # The "Bottleneck": The data is now compressed to just 8 features
        )
        
        # 2. THE DECODER tries to rebuild the original features from the 8-feature bottleneck
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, input_size),
            nn.Sigmoid() # Sigmoid ensures the final output is between 0 and 1 (matching our scaled data!)
        )

    # This function defines how the data flows through the hourglass
    def forward(self, x):
        compressed_data = self.encoder(x)
        reconstructed_data = self.decoder(compressed_data)
        return reconstructed_data

print("Neural Network Architecture Built Successfully!")