library(tidyverse)
library(arrow)
library(janitor)

if (!file.exists("outputs/journeys.parquet")) {
  cat("Run 03_journey_construction.R first to create journeys.parquet\n")
  q()
}

journeys <- read_parquet("outputs/journeys.parquet")
ref_tables <- readRDS("outputs/reference_tables.rds")
diagnosis <- ref_tables$diagnosis

cat("Focus area analysis placeholder.\n")
cat("Uncomment the section matching your chosen focus area.\n\n")

# ========== FOCUS A: DEPRESSION =========
# cat("Focus A: Depression trajectories\n")
# depression_diags <- diagnosis |>
#   filter(grepl("^F3[23]", group_code)) |>
#   pull(diagnosis_value)
#
# focus_journeys <- journeys |>
#   filter(diagnosis_value %in% depression_diags) |>
#   drop_na(median_gap_days)
#
# cat("Depression journeys found:", nrow(focus_journeys), "\n")

# ========== FOCUS B: TRANSPORTATION BARRIERS =========
# cat("Focus B: Transportation barriers and follow-up gaps\n")
# sdoh <- read_csv("data/social_determinants.csv") |> clean_names()
# transport_encounters <- sdoh |>
#   filter(grepl("transportation", display_name, ignore.case = TRUE)) |>
#   distinct(encounter_key, patient_durable_key, answer_text)
#
# focus_journeys <- journeys |>
#   semi_join(transport_encounters, by = "patient_durable_key") |>
#   drop_na(median_gap_days)
#
# cat("Journeys linked to transportation questions:", nrow(focus_journeys), "\n")

# ========== FOCUS C: DIABETES =========
# cat("Focus C: Diabetes journeys and MyChart engagement\n")
# diabetes_diags <- diagnosis |>
#   filter(grepl("^E1[013]", group_code)) |>
#   pull(diagnosis_value)
#
# focus_journeys <- journeys |>
#   filter(diagnosis_value %in% diabetes_diags) |>
#   drop_na(median_gap_days)
#
# cat("Diabetes journeys found:", nrow(focus_journeys), "\n")

# ========== FOCUS D: RURAL VS URBAN =========
# cat("Focus D: Rural vs urban journeys\n")
# cats <- read_csv("data/tigercensuscodes.csv") |> clean_names()
#
# focus_journeys <- journeys |>
#   left_join(cats, by = c("census_block_group_fips_code" = "geoid")) |>
#   drop_na(median_gap_days)
#
# cat("Journeys with census data:", nrow(focus_journeys), "\n")

cat("\nRun EDA in 02_eda.R to decide focus area, then uncomment above.\n")
