## Load required libraries
library(ggplot2)
library(dplyr)

## Load the CSV file
complete_data <- read.csv("Your/path/to/tracking_data.csv")

## Define movie duration and sampling rate
movie_duration <- 10
sampling_rate <- 25
frames_per_interval <- sampling_rate * 60
num_intervals <- floor(movie_duration / 1)

## Create intervals and assign to DataFrame
intervals <- cut(complete_data$frame, breaks = num_intervals, labels = FALSE)
complete_data$time_interval <- intervals

## Calculate the duration each trajectory was present
frame_rate <- 25
summary_df <- complete_data %>%
  group_by(treatment, rep, time_interval, trajectory) %>%
  summarise(
    start_frame = min(frame),
    end_frame = max(frame),
    duration_sec = (end_frame - start_frame) / frame_rate
  )
summary_df <- as.data.frame(summary_df)

## Summarize cumulative duration for each time interval
cumulative_duration_df <- summary_df %>%
  group_by(treatment, rep, time_interval) %>%
  summarise(cumulative_duration_sec = sum(duration_sec))

cumulative_duration_df <- as.data.frame(cumulative_duration_df)

## Calculate statistics
Table <- suppressWarnings(pairwise.wilcox.test(cumulative_duration_df$cumulative_duration_sec, cumulative_duration_df$treatment, "BH"))
Table2 <- Table$p.value
Table3 <- fullPTable(Table2)
lette <- multcompLetters(Table3)$Letters

## Plot cumulative duration over time
ggplot(cumulative_duration_df, aes(x = time_interval, y = cumulative_duration_sec, color = as.factor(treatment))) +
  stat_summary(fun = mean, geom = "line", size = 1) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.2) + 
  scale_x_continuous(limits = c(0, 11), breaks = seq(0, 10, 2), expand = c(0, 0), name = 'Time (min)') +
  scale_y_continuous(limits = c(0, 175), breaks = seq(0, 170, 30), expand = c(0, 0), name = 'Sum duration in the ROI') +
  ylab('Sum duration in the ROI') +
  theme_classic() +
  labs(color = "Treatment") + theme(legend.position = 'none')

ggsave(filename = "Duration.pdf", path = "plot/directory")


