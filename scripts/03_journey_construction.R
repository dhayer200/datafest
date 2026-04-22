library(tidyverse)
library(arrow)
library(janitor)
library(lubridate)

ref_tables <- readRDS("outputs/reference_tables.rds")
patients <- ref_tables$patients
diagnosis <- ref_tables$diagnosis
departments <- ref_tables$departments
providers <- ref_tables$providers

cat("Constructing patient journeys...\n")

encounters <- open_dataset("data/encounters.csv", format = "csv") |>
  filter(PrimaryDiagnosisKey != -1) |>
  select(
    EncounterKey, PatientDurableKey, PrimaryDiagnosisKey,
    Date, AdmissionInstant, DischargeInstant,
    ProviderDurableKey, DepartmentKey,
    IsEdVisit, IsHospitalAdmission, IsInpatientAdmission,
    AdmitYear
  ) |>
  collect() |>
  clean_names() |>
  left_join(
    diagnosis |> select(diagnosis_key, diagnosis_value, group_code, group_name),
    by = c("primary_diagnosis_key" = "diagnosis_key")
  )

encounters <- encounters |>
  mutate(
    date = mdy(date),
    across(ends_with("_instant"), ~ as.POSIXct(., format = "%Y-%m-%d %H:%M:%S", tz = "UTC"))
  )

journeys <- encounters |>
  group_by(patient_durable_key, diagnosis_value, group_code, group_name) |>
  arrange(date) |>
  summarise(
    n_encounters = n(),
    first_date = min(date, na.rm = TRUE),
    last_date = max(date, na.rm = TRUE),
    duration_days = as.integer(last_date - first_date),
    n_providers = n_distinct(provider_durable_key, na.rm = TRUE),
    n_departments = n_distinct(department_key, na.rm = TRUE),
    ed_visits = sum(is_ed_visit, na.rm = TRUE),
    hospital_admissions = sum(is_hospital_admission, na.rm = TRUE),
    inpatient_admissions = sum(is_inpatient_admission, na.rm = TRUE),
    .groups = "drop"
  ) |>
  mutate(
    median_gap_days = NA_integer_,
    max_gap_days = NA_integer_
  )

for (i in seq_len(nrow(journeys))) {
  pt_key <- journeys$patient_durable_key[i]
  diag_val <- journeys$diagnosis_value[i]

  dates <- encounters |>
    filter(
      patient_durable_key == pt_key,
      diagnosis_value == diag_val
    ) |>
    pull(date) |>
    sort()

  if (length(dates) > 1) {
    gaps <- as.integer(diff(dates))
    journeys$median_gap_days[i] <- median(gaps, na.rm = TRUE)
    journeys$max_gap_days[i] <- max(gaps, na.rm = TRUE)
  }
}

journeys <- journeys |>
  left_join(
    patients |> select(
      durable_key, first_race, sex_assigned_at_birth,
      vital_status, my_chart_status, census_block_group_fips_code,
      patient_birth_year_bin, smoking_status
    ),
    by = c("patient_durable_key" = "durable_key")
  )

arrow::write_parquet(journeys, "outputs/journeys.parquet")

cat("\nJourney table created:\n")
cat("Total journeys:", nrow(journeys), "\n")
cat("Unique patients:", n_distinct(journeys$patient_durable_key), "\n")
cat("Unique diagnoses:", n_distinct(journeys$diagnosis_value), "\n")
cat("Median encounters per journey:", median(journeys$n_encounters), "\n")
cat("Median journey duration (days):", median(journeys$duration_days, na.rm = TRUE), "\n")
cat("\nSaved to outputs/journeys.parquet\n")
