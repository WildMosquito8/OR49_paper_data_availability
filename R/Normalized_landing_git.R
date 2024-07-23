## Load required libraries
library(ggplot2)
library(dplyr)
library(ggpubr)
library(caret)
library(rcompanion)
library(multcompView)

## Define the place to save all plots
setwd("Your/path/to/save/plots")

## Load the CSV file
df <- read.csv("Your/path/to/general_visits.csv")
df$time_interval <- df$time_interval + 1
df$t <- as.factor(df$treatment)

## Save df for Qualitative plot
dfquali <- df

## Reorder and rename treatment factor levels
df$treatment <- factor(df$treatment, levels = c('cnt', 'b2'))
levels(df$treatment) <- c('Control', 'Borneol')

## Print the new DataFrame
head(df)

# counting how many trajectories
sum(df$counts[df$t=='cnt'])
sum(df$counts[df$t=='b2'])
## Normalize the data
meancnt <- mean(df$counts[df$treatment == 'Control'])
norm1 <- df
norm1$counts <- norm1$counts / meancnt * 100

## Summary of normalized data
summary(norm1)

## Perform pairwise Wilcoxon test
counts <- norm1$counts
treatment <- norm1$treatment

ress <- pairwise.wilcox.test(counts, treatment, p.adjust.method = 'BH')
print(ress)

Table <- suppressWarnings(pairwise.wilcox.test(counts, treatment, "BH"))
Table2 <- Table$p.value
Table3 <- fullPTable(Table2)
lette <- multcompLetters(Table3)$Letters

## Plot the results
p <- ggbarplot(norm1, x = "treatment", y = "counts", add = "mean_se", palette = "cnt") +
  rotate_x_text(angle = 45) +
  ylab("Normalized trajectory number (%)") +
  xlab("Treatment") +
  scale_y_continuous(expand = c(0, 0), breaks = c(seq(0, 100, by = 25), 100)) +
  theme(plot.title = element_text(hjust = 0.5)) +
  annotate("text", x = 1:2, y = 70, label = lette)

print(p)
ggsave("normalized_landing_during10_minutes.pdf", width = 8.29, height = 11.67, units = "in")

## Percentage reduction
meanSol <- mean(norm1$counts[norm1$t == 'cnt'])
meanDEET <- mean(norm1$counts[norm1$t == 'b2'])

percentageReduction <- c()
for (i in levels(norm1$t)) {
  reduction <- abs(mean(norm1$counts[norm1$t == i]) / meanSol * 100 - 100)
  percentageReduction <- c(percentageReduction, reduction)
}

percentageReduction <- data.frame(treatment = levels(norm1$t), percentageReduction)


## Create ggplot object with dodged boxplots
objects_by_treatment_and_rep_plot <- ggplot(df, aes(x = treatment, y = counts, color = rep)) +
  geom_jitter(aes(colour = rep)) + theme_classic() + 
  scale_y_continuous(expand = c(0, 0), limits = c(0, 100))

print(objects_by_treatment_and_rep_plot)
ggsave("jitterplot_of_reps.pdf", width = 8.29, height = 11.67, units = "in")

## Boxplot
ggplot(df, aes(x = treatment, y = counts, color = rep)) +
  geom_boxplot() + theme_classic() + 
  scale_y_continuous(expand = c(0, 0), limits = c(0, 100))

ggsave("boxplot_of_reps.pdf", width = 8.29, height = 11.67, units = "in")

## Line plot of counts over time
ggplot(df, aes(x = time_interval, y = counts, color = as.factor(treatment))) +
  stat_summary(fun = mean, geom = "line", size = 1) + 
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.2) + 
  theme_classic() + 
  ylab("Mean Trajectory counts") + 
  xlab("Time (min)") + 
  theme(legend.position = 'none') +
  scale_x_continuous(limits = c(0, 11), breaks = seq(0, 10, 2), expand = c(0, 0))+
  scale_y_continuous(expand = c(0, 0),breaks = seq(0, 60, 10), limits = c(0, 75))

ggsave("average_detections_dynamics.pdf", width = 8.29, height = 11.67, units = "in")
