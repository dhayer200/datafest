import pandas as pd
import os

print("Loading data...")

encounters = pd.read_csv("data/encounters.csv")
patients = pd.read_csv("data/patients.csv")
diagnosis = pd.read_csv("data/diagnosis.csv")
departments = pd.read_csv("data/departments.csv")
providers = pd.read_csv("data/providers.csv")
social_determinants = pd.read_csv("data/social_determinants.csv")
tigercensuscodes = pd.read_csv("data/tigercensuscodes.csv")

for df in [encounters, patients, diagnosis, departments, providers, social_determinants, tigercensuscodes]:
    df.columns = [col.lower() for col in df.columns]

print("\nSummary of loaded data:")
print(f"encounters:           {len(encounters)} rows")
print(f"patients:             {len(patients)} rows")
print(f"diagnosis:            {len(diagnosis)} rows")
print(f"departments:          {len(departments)} rows")
print(f"providers:            {len(providers)} rows")
print(f"social_determinants:  {len(social_determinants)} rows")
print(f"tigercensuscodes:     {len(tigercensuscodes)} rows")

os.makedirs("outputs", exist_ok=True)

patients.to_pickle("outputs/patients.pkl")
diagnosis.to_pickle("outputs/diagnosis.pkl")
departments.to_pickle("outputs/departments.pkl")
providers.to_pickle("outputs/providers.pkl")

print("\nReference tables saved to outputs/")
