## Load required libraries
library(ggplot2)
library(dplyr)

## Load the CSV file
df <- read.csv("Your/path/to/tracking_data.csv")
df = df[order(df$frame),]
## Reorder and rename treatment factor levels
df$treatment <- factor(df$treatment, levels = c('cnt', 'b2'))
df$x <- df$x * 1280
df$y <- df$y * 720

## Save original data
b <- df

## Plot trajectories for each treatment and replicate
for (i in unique(df$treatment)) {
  for (rep in unique(df$rep)) {
    filtered_df <- df[df$treatment == i & df$rep == rep,]
    num_trajectories <- length(unique(filtered_df$trajectory))
    
    p <- ggplot(filtered_df, aes(x = x, y = y, color = as.factor(trajectory))) +
      geom_path(size = 0.5) + theme_classic() +
      labs(title = paste(i,rep, "trajectories")) + theme(legend.position = 'none') +
      scale_y_continuous(expand = c(0, 0), limits = c(0, 720), name = "Y axis") +
      scale_x_continuous(limits = c(0, 1280), expand = c(0, 0), name = "X axis") +
      coord_fixed(ratio = 1) +
      annotate("text", x = 250, y = 600, label = paste("Trajectories:", num_trajectories), 
               hjust = 1.1, vjust = 2, size = 4, color = "black")
    
    ggsave(filename = paste0(i, "_", rep, " traj", ".pdf"), plot = p, 
           path = "path/to/Supplementary/plots")
  }
}

# Calculate detections per frame
detections_per_frame <- df %>%
  group_by(frame,treatment,rep) %>%
  summarise(detections = n())

# Print the results
detections_per_frame = as.data.frame(detections_per_frame)
print(detections_per_frame)


detections_per_frame$min <- detections_per_frame$frame / 25 / 60
max(df$min)

## Define repetitions
repetitions <- c("rep1", "rep2", "rep3")

## Plot bar charts for each repetition and treatment
for (rep in repetitions) {
  # Create the plot for treatment "cnt"
  plot_cnt <- ggplot(detections_per_frame[detections_per_frame$rep == rep & detections_per_frame$treatment == "cnt",], aes(x = min, y = detections, color = as.factor(detections))) +
    geom_bar(stat = "identity", aes(fill = as.factor(detections))) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_x_continuous(limits = c(0, 10), breaks = c(0, 2, 4, 6, 8, 10), expand = c(0, 0)) +
    theme_minimal() +
    scale_color_grey(start = 0.9, end = 0) +
    scale_fill_grey(start = 0.9, end = 0) +
    theme_classic()
  
  # Save the plot as PDF
  filename_cnt <- paste0("cnt_", rep, ".pdf")
  ggsave(filename_cnt, plot = plot_cnt, width = 5.83, height = 8.27, units = "in", path = "path/to/Supplementary/plots")
  
  # Create the plot for treatment "b2"
  plot_b2 <-ggplot(detections_per_frame[detections_per_frame$rep == rep & detections_per_frame$treatment == "b2",], aes(x = min, y = detections, color = as.factor(detections))) +
    geom_bar(stat = "identity", aes(fill = as.factor(detections))) +
    scale_y_continuous(expand = c(0, 0)) +
    scale_x_continuous(limits = c(0, 10), breaks = c(0, 2, 4, 6, 8, 10), expand = c(0, 0)) +
    theme_minimal() +
    scale_color_grey(start = 0.9, end = 0) +
    scale_fill_grey(start = 0.9, end = 0) +
    theme_classic()
  
  # Save the plot as PDF
  filename_b2 <- paste0("borneol_", rep, ".pdf")
  ggsave(filename_b2, plot = plot_b2, width = 5.83, height = 8.27, units = "in", path = "path/to/Supplementary/plots")
}
