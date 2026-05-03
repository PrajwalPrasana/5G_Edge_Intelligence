import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

print("--- 5G Data Preprocessing Started ---\n")

# LOAD THE DATA
file_path = '5G_traffic_data.csv'
print("[1/4] Loading dataset...")

try:
    df = pd.read_csv(file_path)
    print(f"      Success! Loaded {df.shape[0]} rows and {df.shape[1]} features.")
except FileNotFoundError:
    print(f"      ERROR: Cannot find {file_path}. Make sure it's in the same folder!")
    exit()

#CLEAN THE DATA (Remove junk)
print("[2/4] Cleaning data (removing useless tracking columns)...")

# We drop columns like 'Seq' (sequence number) because they are just 
# index trackers and don't represent actual network behavior.
cols_to_drop = ['Unnamed: 0', 'Seq']
df_clean = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# We only want it to learn from raw network traffic features.
columns_to_drop = ['Label', 'Attack Tool', 'Attack Type', 'Cause']
df_clean = df_clean.drop(columns=columns_to_drop, errors='ignore')

# FIX MISSING & TEXT DATA
print("[3/4] Fixing missing values and converting text to numbers...")

# Separate the columns into "numbers" and "text"
numeric_cols = df_clean.select_dtypes(include=['number']).columns
text_cols = df_clean.select_dtypes(exclude=['number']).columns

# Fill empty number gaps with 0, and empty text gaps with 'Unknown'
df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
df_clean[text_cols] = df_clean[text_cols].fillna('Unknown')

# AI models cannot read text (like "UDP" or "TCP"). 
# LabelEncoder converts these text words into numbers (e.g., UDP = 1, TCP = 2)
encoder = LabelEncoder()
for col in text_cols:
    df_clean[col] = encoder.fit_transform(df_clean[col].astype(str))

# SCALE THE DATA (Normalization)
print("[4/4] Scaling all network features to a 0-to-1 range...")

# If bandwidth is 15,000,000 and jitter is 2, the AI will get biased toward the bigger number.
# MinMaxScaler shrinks EVERY number to a decimal between 0.0 and 1.0 so the AI treats them fairly.
scaler = MinMaxScaler()
scaled_values = scaler.fit_transform(df_clean)

# Put the final numbers back into a DataFrame
df_final = pd.DataFrame(scaled_values, columns=df_clean.columns)

print("\n--- Preprocessing Complete! ---")
print("Here is a peek at the first 3 rows of your AI-ready data:\n")

# We only print the first 5 columns so it doesn't clutter your screen
print(df_final.iloc[:3, :5])