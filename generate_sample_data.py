import os
import pandas as pd

DATA_FOLDER = "data"
SAMPLE_FOLDER = "sample_data"
SAMPLE_SIZE = 700
RANDOM_STATE = 42   

os.makedirs(SAMPLE_FOLDER, exist_ok=True)

for file in os.listdir(DATA_FOLDER):

    if not file.endswith(".csv"):
        continue

    file_path = os.path.join(DATA_FOLDER, file)

    print(f"Processing {file}...")

    df = pd.read_csv(file_path)

    if len(df) < SAMPLE_SIZE:
        print(f"Warning: {file} has only {len(df)} rows. Taking full dataset.")
        sample_df = df.copy()
    else:
        sample_df = df.sample(
            n=SAMPLE_SIZE,
            random_state=RANDOM_STATE
        )

    sample_file_path = os.path.join(SAMPLE_FOLDER, file)

    sample_df.to_csv(sample_file_path, index=False)

    print(f"Sample saved → {sample_file_path}")

print("\n Sample data generation complete.")
