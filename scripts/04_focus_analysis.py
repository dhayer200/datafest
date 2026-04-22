import pandas as pd
import numpy as np

print("=" * 80)
print("FOCUS ANALYSIS: Type 2 Diabetes, Age 60-80, Transportation Barriers, Urban/Rural")
print("=" * 80)

journeys = pd.read_parquet("outputs/journeys.parquet")
sdoh = pd.read_csv("data/social_determinants.csv", low_memory=False)
sdoh.columns = [c.lower() for c in sdoh.columns]

diabetes_code = "ICD-10-CM: E11"
focus_journeys = journeys[journeys['groupcode'] == diabetes_code].copy()
print(f"\n1. Diabetes journeys (E11): {len(focus_journeys):,}")

focus_journeys = focus_journeys[focus_journeys['n_encounters'] > 1]
print(f"2. Multi-encounter journeys: {len(focus_journeys):,}")

focus_journeys = focus_journeys[(focus_journeys['patientbirthyearbin'] >= 1945) &
                                (focus_journeys['patientbirthyearbin'] <= 1965)]
print(f"3. Age 60-80 (born 1945-1965): {len(focus_journeys):,}")

transport_sdoh = sdoh[sdoh['domain'] == 'Transportation Needs'].copy()
transport_sdoh.columns = [c.lower() for c in transport_sdoh.columns]
transport_barrier_patients = transport_sdoh[transport_sdoh['answertext'] == 'Yes']['patientdurablekey'].unique()
print(f"4. Patients with transportation barriers: {len(transport_barrier_patients):,}")

focus_journeys['has_transport_barrier'] = focus_journeys['patientdurablekey'].isin(transport_barrier_patients)
print(f"   - In focus cohort with barrier: {focus_journeys['has_transport_barrier'].sum():,}")
print(f"   - In focus cohort without barrier: {(~focus_journeys['has_transport_barrier']).sum():,}")

focus_journeys['geography'] = focus_journeys['censusblockgroupfipscode'].apply(
    lambda x: 'Urban' if str(x).startswith('20177') else ('Rural' if str(x) == '*Unspecified' else 'Other')
)
focus_journeys = focus_journeys[focus_journeys['geography'] != 'Other']
print(f"5. With valid geography (urban/rural): {len(focus_journeys):,}")
print(f"   - Urban: {(focus_journeys['geography'] == 'Urban').sum():,}")
print(f"   - Rural: {(focus_journeys['geography'] == 'Rural').sum():,}")

print("\n" + "=" * 80)
print("SUMMARY STATISTICS BY GROUP")
print("=" * 80)

for barrier in [False, True]:
    for geo in ['Urban', 'Rural']:
        subset = focus_journeys[(focus_journeys['has_transport_barrier'] == barrier) &
                               (focus_journeys['geography'] == geo)]
        if len(subset) > 0:
            barrier_label = "With barrier" if barrier else "No barrier"
            print(f"\n{geo} - {barrier_label} (n={len(subset):,})")
            print(f"  Median gap days: {subset['median_gap_days'].median():.0f}")
            print(f"  Mean gap days: {subset['median_gap_days'].mean():.0f}")
            print(f"  Median journey duration (days): {subset['duration_days'].median():.0f}")
            print(f"  Median encounters per journey: {subset['n_encounters'].median():.0f}")

print("\n" + "=" * 80)
print("SAVING FOCUS DATASET")
print("=" * 80)

focus_journeys.to_parquet("outputs/focus_diabetes.parquet", index=False)
print(f"✓ Saved: outputs/focus_diabetes.parquet ({len(focus_journeys):,} journeys)")
