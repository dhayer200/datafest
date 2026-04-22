import pandas as pd
import numpy as np

print("Loading data...")
encounters = pd.read_csv("data/encounters.csv")
patients = pd.read_csv("data/patients.csv")
diagnosis = pd.read_csv("data/diagnosis.csv")

for df in [encounters, patients, diagnosis]:
    df.columns = [col.lower() for col in df.columns]

print("Constructing patient journeys...")

encounters = encounters[encounters['primarydiagnosiskey'] != -1].copy()
encounters['date'] = pd.to_datetime(encounters['date'])

encounters = encounters.merge(
    diagnosis[['diagnosiskey', 'diagnosisvalue', 'groupcode', 'groupname']],
    left_on='primarydiagnosiskey',
    right_on='diagnosiskey',
    how='left'
)

encounters = encounters.sort_values(['patientdurablekey', 'diagnosisvalue', 'date'])

journeys = encounters.groupby(['patientdurablekey', 'diagnosisvalue', 'groupcode', 'groupname']).agg({
    'encounterkey': 'count',
    'date': ['min', 'max'],
    'providerdurablekey': 'nunique',
    'departmentkey': 'nunique',
    'isedvisit': 'sum',
    'ishospitaladmission': 'sum',
    'isinpatientadmission': 'sum'
}).reset_index()

journeys.columns = ['patientdurablekey', 'diagnosisvalue', 'groupcode', 'groupname',
                   'n_encounters', 'first_date', 'last_date', 'n_providers', 'n_departments',
                   'ed_visits', 'hospital_admissions', 'inpatient_admissions']

journeys['duration_days'] = (journeys['last_date'] - journeys['first_date']).dt.days

encounters['gap_days'] = encounters.groupby(['patientdurablekey', 'diagnosisvalue'])['date'].diff().dt.days

gap_stats = encounters.groupby(['patientdurablekey', 'diagnosisvalue'])['gap_days'].agg(
    median_gap_days=('median'),
    max_gap_days=('max')
).reset_index()

journeys = journeys.merge(gap_stats, on=['patientdurablekey', 'diagnosisvalue'], how='left')

journeys = journeys.merge(
    patients[['durablekey', 'firstrace', 'sexassignedatbirth', 'vitalstatus',
             'mychartstatus', 'censusblockgroupfipscode', 'patientbirthyearbin', 'smokingstatus']],
    left_on='patientdurablekey',
    right_on='durablekey',
    how='left'
)

journeys.to_parquet("outputs/journeys.parquet", index=False)

print(f"\nJourney table created:")
print(f"Total journeys: {len(journeys):,}")
print(f"Unique patients: {journeys['patientdurablekey'].nunique():,}")
print(f"Unique diagnoses: {journeys['diagnosisvalue'].nunique():,}")
print(f"Median encounters per journey: {journeys['n_encounters'].median():.0f}")
print(f"Median journey duration (days): {journeys['duration_days'].median():.0f}")
print(f"\nSaved to outputs/journeys.parquet")
