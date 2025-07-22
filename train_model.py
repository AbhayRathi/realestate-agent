import pandas as pd
import json

csv_file = ["real_estate_data_train.csv"]

dataset = []

for file in csv_files:
    df = pd.read_csv(file)
    
    for _, row in df.iterrows():
        dataset.append({
            "input": row["Query Example"],
            "output": row["AI-Generated Response"]
        })

# Save formatted data for fine-tuning
with open("training_data.json", "w") as f:
    json.dump(dataset, f, indent=4)

print("✅ Training data saved: training_data.json")