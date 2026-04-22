library(tidyverse)
library(arrow)
library(janitor)

source("scripts/01_load_data.R")

cat("\n========== ENCOUNTERS ==========\n")
cat("Shape:", nrow(encounters |> select(1) |> collect()), "rows,", ncol(encounters |> head(1) |> collect()), "cols\n")
cat("Missingness (%):\n")
encounters |>
  select(1:10) |>
  summarise(across(everything(), ~ mean(is.na(.)))) |>
  collect() |>
  pivot_longer(everything(), names_to = "column", values_to = "pct_missing") |>
  arrange(desc(pct_missing)) |>
  print()

cat("\nEncounter types (Type):\n")
encounters |>
  group_by(type) |>
  count() |>
  arrange(desc(n)) |>
  collect() |>
  print()

cat("\nBy admission year:\n")
encounters |>
  group_by(admit_year) |>
  count() |>
  collect() |>
  print()

cat("\n========== PATIENTS ==========\n")
cat("Shape:", nrow(patients), "rows,", ncol(patients), "cols\n")
cat("Missingness (%):\n")
patients |>
  summarise(across(everything(), ~ mean(is.na(.)))) |>
  pivot_longer(everything(), names_to = "column", values_to = "pct_missing") |>
  arrange(desc(pct_missing)) |>
  print()

cat("\nRace distribution:\n")
patients |>
  count(first_race, sort = TRUE) |>
  print()

cat("\nMyChart status:\n")
patients |>
  count(my_chart_status, sort = TRUE) |>
  print()

cat("\n========== DIAGNOSIS ==========\n")
cat("Shape:", nrow(diagnosis), "rows\n")
cat("Top 25 diagnosis groups by usage in encounters:\n")
encounters |>
  left_join(
    diagnosis |> select(diagnosis_key, group_code, group_name),
    by = c("primary_diagnosis_key" = "diagnosis_key")
  ) |>
  group_by(group_code, group_name) |>
  count() |>
  arrange(desc(n)) |>
  head(25) |>
  collect() |>
  print()

cat("\n========== SOCIAL DETERMINANTS ==========\n")
cat("Shape:", nrow(social_determinants |> select(1) |> collect()), "rows\n")
cat("Domains:\n")
social_determinants |>
  group_by(domain) |>
  count() |>
  arrange(desc(n)) |>
  collect() |>
  print()

cat("\nPatient coverage (% with any SDoH response):\n")
n_patients_with_sdoh <- social_determinants |>
  distinct(patient_durable_key) |>
  collect() |>
  nrow()
pct_coverage <- round(100 * n_patients_with_sdoh / nrow(patients), 2)
cat(n_patients_with_sdoh, "of", nrow(patients), "patients =", pct_coverage, "%\n")
