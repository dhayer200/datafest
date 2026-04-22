# Geographic Disparities in Diabetes Care
## ASA DataFest 2026 Analysis

A data analysis examining whether transportation barriers explain gaps in diabetes follow-up care at Stormont Vail Health, a rural health system serving 19 counties in Northeast Kansas.

**TL;DR**: Transportation barriers aren't the real problem. Geography is. Rural patients get fundamentally different care patterns (shorter, more episodic) compared to urban patients. Plus, we can't even see the full picture - 41% of rural patients are missing from the social determinants data entirely.

## The Problem

Stormont Vail Health serves a population spread across mostly rural Kansas, from Topeka (125k people) to counties with under 1,000 residents. Diabetes patients need regular follow-ups every 3 months to manage their condition properly. But healthcare access isn't uniform.

The obvious question: do transportation barriers prevent rural patients from keeping appointments? This analysis digs into whether that's actually what's going on.

## The Data

- 2.8 million patient encounters from 2022-2025
- Focused on Type 2 diabetes patients ages 60-80
- 12,963 diabetes journeys across 8,698 unique patients
- Geographic split: urban (Shawnee County, n=9,228) vs rural (19 counties, n=3,735)
- Social determinants data from survey responses

## Key Findings

1. **Barriers don't explain the gap** - Urban and rural patients with transportation barriers actually have similar (or shorter) appointment gaps compared to those without barriers. Urban no barrier: 92 days. Urban with barrier: 79 days. Rural shows the same pattern.

2. **The real issue is rural patients disappear from the data** - 41% of rural patients lack valid census block data, which means we can't classify them as having barriers or not. That's a data quality problem that masks the real picture.

3. **Rural care looks different** - Patients in rural areas have much shorter care journeys (258 days) compared to urban patients (749 days). This suggests they're getting acute care visits rather than continuous chronic disease management.

## What This Shows

- How to analyze patient journey data across a health system
- Social determinants of health (SDoH) in action - and what happens when data is missing
- Why chart choice matters for different audiences (heatmaps beat violin plots for decision makers)
- How to tell a story when the obvious hypothesis is wrong (barriers aren't the problem)

## Important Notes on De-identification

The data files included here are derived from de-identified encounter data from Stormont Vail Health. No personally identifiable information is included. All analysis respects HIPAA requirements for handling healthcare data.

## Competition Context

This was submitted to ASA DataFest 2026. The analysis ranks the problem (transportation barriers) but finds that geography itself is the deeper issue. That reframing from "how do we overcome barriers" to "how do we serve a dispersed population" is where the value sits.

## Next Steps for Stormont Vail

1. Close the 41% rural data gap by completing SDoH surveys in rural clinics
2. Investigate why rural journeys are so short - are patients getting preventive care or only emergency/acute visits?
3. Pilot rural-focused interventions: telehealth for continuity, care coordination across county lines, patient navigation services

## Authors

DataFest 2026 Team - Stormont Vail Health track

## License

This analysis is provided as-is for educational and research purposes. If you're using this methodology with your own health system data, verify HIPAA compliance and institutional approval before sharing results publicly.
