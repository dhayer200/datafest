# R Cheat Sheet for DataFest

> Everything you actually need. Skim once before 5pm; keep it open in a second monitor.

---

## 1. Open-of-session ritual (paste into RStudio every time)

```r
library(tidyverse)     # dplyr + ggplot2 + readr + tidyr + stringr + purrr
library(lubridate)     # dates & times
library(janitor)       # clean_names(), tabyl()
library(scales)        # comma(), dollar(), percent() for axis labels

# Load your data
df <- read_csv("path/to/data.csv") |> clean_names()

# First look
glimpse(df)            # types + first values of every column
head(df, 10)           # top 10 rows
summary(df)            # min/median/mean/max + NA counts
nrow(df); ncol(df)     # size
names(df)              # column names
```

`clean_names()` is magic: turns `"Order Total $"` into `order_total` so you don't fight with spaces and symbols.

---

## 2. The 10 dplyr verbs (90% of data wrangling)

The pipe `|>` (or `%>%`) means "take the thing on the left, feed it into the function on the right."

```r
df |>
  filter(age >= 18, country == "USA")      # keep rows matching conditions
  select(name, age, income)                # keep columns
  mutate(income_k = income / 1000)         # create/modify columns
  group_by(country) |> summarize(          # aggregate
      n = n(),
      avg_income = mean(income, na.rm = TRUE),
      median_age = median(age, na.rm = TRUE)
  )
  arrange(desc(avg_income))                # sort (desc = biggest first)
  count(category, sort = TRUE)             # group_by + summarize(n=n()) shortcut
  distinct(user_id)                        # unique rows
  slice_max(income, n = 10)                # top-10 rows by column
  rename(new_name = old_name)              # rename columns
  left_join(other_df, by = "user_id")      # merge two tables
```

**Remember:** `na.rm = TRUE` everywhere there's a mean/median/sum, or you get `NA`.

---

## 3. ggplot2 recipes (copy, swap columns, done)

Every plot: `ggplot(data, aes(x = ..., y = ...)) + geom_...()`

```r
# Histogram — distribution of ONE numeric variable
ggplot(df, aes(x = age)) +
  geom_histogram(bins = 30, fill = "steelblue") +
  labs(title = "Age distribution", x = "Age", y = "Count")

# Bar chart — counts of a categorical variable
ggplot(df, aes(x = fct_infreq(category))) +   # fct_infreq sorts by frequency
  geom_bar() +
  coord_flip()                                # horizontal bars = readable labels

# Scatter — relationship between two numerics
ggplot(df, aes(x = age, y = income)) +
  geom_point(alpha = 0.3) +                   # alpha = transparency for big data
  geom_smooth(method = "lm")                  # add trend line

# Boxplot — numeric split by category
ggplot(df, aes(x = region, y = income)) +
  geom_boxplot()

# Line chart — something over time
ggplot(df, aes(x = date, y = sales)) +
  geom_line() +
  scale_y_continuous(labels = comma)          # 1,000,000 instead of 1e+06

# Facets — one chart per category
ggplot(df, aes(x = age)) +
  geom_histogram() +
  facet_wrap(~ region)                        # mini-plot per region
```

**Save any chart:** `ggsave("plot.png", width = 8, height = 5, dpi = 300)`

**Polish:** always add `labs(title=, subtitle=, x=, y=, caption=)`. Judges love clear labels.

---

## 4. Missing data (you WILL have NAs)

```r
df |> summarize(across(everything(), ~ sum(is.na(.)))) |> glimpse()   # count NAs per column
df |> drop_na(income)                           # drop rows where income is NA
df |> mutate(income = replace_na(income, 0))    # replace NA with a value
```

---

## 5. Dates (lubridate)

```r
df <- df |> mutate(
  date = ymd(date_string),          # also mdy(), dmy() depending on format
  year = year(date),
  month = month(date, label = TRUE),
  weekday = wday(date, label = TRUE)
)
```

---

## 6. Quick statistical tests (one-liners)

```r
cor(df$x, df$y, use = "complete.obs")                  # correlation
t.test(income ~ gender, data = df)                     # compare 2 groups
summary(lm(income ~ age + education, data = df))       # linear regression
chisq.test(table(df$category_a, df$category_b))        # categorical association
```

---

## 7. Working with Claude (you!) during DataFest

1. **Give me the schema first.** Paste the output of `glimpse(df)` in your first message. I can't help if I don't know what columns exist.
2. **Paste errors verbatim.** Copy the whole red error block — don't paraphrase.
3. **Ask for one step at a time.** "Show me how to plot X vs Y by group" is better than "do the whole analysis."
4. **Tell me the sponsor's question.** DataFest prompts are deliberately vague; the exact wording shapes the analysis.
5. **When something breaks, ask "why".** I'll translate stats/code to plain English.

---

## 8. Panic button: "I have no idea where to start"

Copy this into RStudio and change `df` to your dataset name:

```r
# 1. Shape & types
glimpse(df)

# 2. Missing data map
df |> summarize(across(everything(), ~ mean(is.na(.)))) |> glimpse()

# 3. Numeric summaries
df |> select(where(is.numeric)) |> summary()

# 4. Categorical counts (top categories of each)
df |> select(where(is.character)) |>
  map(~ sort(table(.x), decreasing = TRUE) |> head(10))

# 5. A default-looking plot of every numeric column
df |> select(where(is.numeric)) |>
  pivot_longer(everything()) |>
  ggplot(aes(x = value)) +
    geom_histogram(bins = 30) +
    facet_wrap(~ name, scales = "free")
```

Run all 5 blocks. Now you've done EDA — you know your data.

---

## 9. Presentation tips (judges care more about these than code)

- **One headline insight.** If your team can't say your finding in one sentence, narrow down.
- **Two to three killer charts > ten okay charts.**
- **Every chart: title, clear axis labels, legend, source note.**
- **"So what?" test.** For each slide, answer: why should the sponsor care?
- **Start the slide deck by Saturday lunch**, not Sunday morning.

---

## 10. Keyboard shortcuts (RStudio)

| Shortcut | Action |
|---|---|
| `Cmd + Enter` | Run current line / selection |
| `Cmd + Shift + Enter` | Run whole script |
| `Cmd + Shift + M` | Insert `|>` pipe |
| `Cmd + /` | Comment/uncomment |
| `Cmd + Shift + C` | Comment/uncomment block |
| `Alt + -` | Insert `<-` (assignment) |
| `Ctrl + L` | Clear console |

---

Good luck. Breathe. Ask for help early and often.
