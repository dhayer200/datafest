library(tidyverse)
library(scales)
library(arrow)

if (!file.exists("outputs/journeys.parquet")) {
  cat("Run 03_journey_construction.R first to create journeys.parquet\n")
  q()
}

journeys <- read_parquet("outputs/journeys.parquet")

cat("Placeholder for presentation charts.\n")
cat("After choosing a focus area in 04_focus_analysis.R, populate this script.\n\n")

# ========== HEADLINE CHART ==========
# p1 <- focus_journeys |>
#   ggplot(aes(x = median_gap_days)) +
#   geom_histogram(bins = 30, fill = "steelblue") +
#   labs(
#     title = "Distribution of time between visits",
#     subtitle = "[Add your focus area context here]",
#     x = "Median days between visits",
#     y = "Number of journeys"
#   ) +
#   theme_minimal()
#
# ggsave("outputs/plot_headline.png", p1, width = 8, height = 5, dpi = 300)

# ========== STRATIFICATION CHART ==========
# p2 <- focus_journeys |>
#   ggplot(aes(x = [stratification_var], y = median_gap_days)) +
#   geom_boxplot(fill = "salmon") +
#   labs(
#     title = "Gap distribution by [variable]",
#     x = "[Variable]",
#     y = "Median days between visits"
#   ) +
#   theme_minimal()
#
# ggsave("outputs/plot_stratification.png", p2, width = 8, height = 5, dpi = 300)

# ========== CONTEXT CHART ==========
# p3 <- focus_journeys |>
#   count([grouping_var]) |>
#   ggplot(aes(x = [grouping_var], y = n)) +
#   geom_col(fill = "lightblue") +
#   labs(
#     title = "Patient count by group",
#     x = "[Variable]",
#     y = "Number of patients"
#   ) +
#   theme_minimal()
#
# ggsave("outputs/plot_context.png", p3, width = 8, height = 5, dpi = 300)

cat("Uncomment sections above when focus area is chosen.\n")
