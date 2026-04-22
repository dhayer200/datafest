library(tidyverse)
library(arrow)
library(janitor)
library(lubridate)

cat("Loading data...\n")

encounters <- open_dataset("data/encounters.csv", format = "csv")

patients <- read_csv("data/patients.csv", col_types = cols(
  DurableKey = col_integer(),
  CensusBlockGroupFipsCode = col_character(),
  FirstRace = col_character(),
  MaritalStatus = col_character(),
  MyChartStatus = col_character(),
  OmbEthnicity = col_character(),
  OmbRace = col_character(),
  SexAssignedAtBirth = col_character(),
  SexualOrientation = col_character(),
  SmokingStatus = col_character(),
  VitalStatus = col_character(),
  PatientBirthYearBin = col_integer()
), show_col_types = FALSE) |>
  clean_names()

diagnosis <- read_csv("data/diagnosis.csv", col_types = cols(
  DiagnosisKey = col_integer(),
  DiagnosisValue = col_character(),
  GroupCode = col_character()
), show_col_types = FALSE) |>
  clean_names()

departments <- read_csv("data/departments.csv", show_col_types = FALSE) |>
  clean_names()

providers <- read_csv("data/providers.csv", show_col_types = FALSE) |>
  clean_names()

social_determinants <- open_dataset("data/social_determinants.csv", format = "csv")

tigercensuscodes <- read_csv("data/tigercensuscodes.csv", show_col_types = FALSE) |>
  clean_names()

cat("\nSummary of loaded data:\n")
cat("encounters:           ", nrow(encounters |> select(1) |> collect()), "rows\n")
cat("patients:             ", nrow(patients), "rows\n")
cat("diagnosis:            ", nrow(diagnosis), "rows\n")
cat("departments:          ", nrow(departments), "rows\n")
cat("providers:            ", nrow(providers), "rows\n")
cat("social_determinants:  ", nrow(social_determinants |> select(1) |> collect()), "rows\n")
cat("tigercensuscodes:     ", nrow(tigercensuscodes), "rows\n")

dir.create("outputs", showWarnings = FALSE)
saveRDS(list(
  patients = patients,
  diagnosis = diagnosis,
  departments = departments,
  providers = providers
), "outputs/reference_tables.rds")

cat("\nReference tables saved to outputs/reference_tables.rds\n")
