## Load required libraries
library(ggplot2)
library(dplyr)
library(ggpubr)
library(caret)
library(rcompanion)
library(multcompView)

## Load the CSV file
df <- read.csv("Your/path/to/tracking_data.csv")
df = df[order(df$frame),]
## Reorder and rename treatment factor levels
df$treatment <- factor(df$treatment, levels = c('cnt', 'b2'))
df$x <- df$x * 1280
df$y <- df$y * 720

## Save original data
b <- df

## Change factor names by assigning new names to the levels
levels(df$treatment) <- c("Control", "Borneol")


## Define movie duration and sampling rate
movie_duration <- 10
sampling_rate <- 25
frames_per_interval <- sampling_rate * 60
num_intervals <- floor(movie_duration / 1)

## Create intervals and assign to DataFrame
intervals <- cut(df$frame, breaks = num_intervals, labels = FALSE)
df$time_interval <- intervals
b$time_interval <- intervals

## Calculate the length of a trajectory
calculate_length <- function(x, y) {
  sum(sqrt(diff(x)^2 + diff(y)^2))
}

## Summarize lengths of trajectories
summary_df <- df %>%
  group_by(treatment, rep, time_interval, trajectory) %>%
  summarise(length = calculate_length(x, y))

## Filter out short trajectories
summary_df <- summary_df[summary_df$length > 5,]

## Summarize lengths by treatment, rep, and time interval
summary <- aggregate(length ~ treatment + rep + time_interval, data = summary_df, sum)

## Perform pairwise Wilcoxon test
Table <- suppressWarnings(pairwise.wilcox.test(summary$length, summary$treatment, "BH"))
Table2 <- Table$p.value
Table3 <- fullPTable(Table2)
lettef <- multcompLetters(Table3)$Letters

## Calculate length in mm
summary$length_cm <- summary$length / 338 * 20 /10

## Plot summarized data
ggplot(summary, aes(x = treatment, y = length_cm, color = treatment)) +
  geom_boxplot() +geom_jitter()+ theme_classic() +
  xlab(" ")
ggsave(filename = "Distance.pdf", path = "plot/directory")

