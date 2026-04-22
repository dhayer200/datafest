import pandas as pd

print("Loading data...")
encounters = pd.read_csv("data/encounters.csv")
patients = pd.read_csv("data/patients.csv")
diagnosis = pd.read_csv("data/diagnosis.csv")
social_determinants = pd.read_csv("data/social_determinants.csv")

for df in [encounters, patients, diagnosis, social_determinants]:
    df.columns = [col.lower() for col in df.columns]

print("\n========== ENCOUNTERS ==========")
print(f"Shape: {len(encounters)} rows, {len(encounters.columns)} cols")
print("\nEncounter types (top 10):")
print(encounters['type'].value_counts().head(10))
print("\nBy admission year:")
print(encounters['admityear'].value_counts().sort_index())

print("\n========== PATIENTS ==========")
print(f"Shape: {len(patients)} rows, {len(patients.columns)} cols")
print("\nRace distribution (top 10):")
print(patients['firstrace'].value_counts().head(10))
print("\nMyChart status:")
print(patients['mychartstatus'].value_counts())

print("\n========== DIAGNOSIS ==========")
print(f"Total diagnoses: {len(diagnosis)}")
print("\nTop 25 diagnosis groups by frequency in encounters:")
enc_diag = encounters.merge(
    diagnosis[['diagnosiskey', 'groupcode', 'groupname']],
    left_on='primarydiagnosiskey',
    right_on='diagnosiskey',
    how='left'
)
print(enc_diag.groupby(['groupcode', 'groupname']).size().sort_values(ascending=False).head(25).to_frame(name='count'))

print("\n========== SOCIAL DETERMINANTS ==========")
print(f"Shape: {len(social_determinants)} rows")
print("\nDomains:")
print(social_determinants['domain'].value_counts())

n_patients_with_sdoh = social_determinants['patientdurablekey'].nunique()
pct_coverage = round(100 * n_patients_with_sdoh / len(patients), 2)
print(f"\nPatient coverage: {n_patients_with_sdoh} of {len(patients)} patients = {pct_coverage}%")
