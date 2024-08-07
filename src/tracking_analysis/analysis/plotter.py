import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from src.tracking_analysis.analysis.time_calculator import TimeUnitsCreator

class Plotter:
    def __init__(self, df,config):
        self.df = df
        self.config = config
        self.output_plot_dir = config['analyse_output']['plots_directory']
        self.df_time_units = None
        self.create_directory()

    def create_directory(self):
        os.makedirs(self.output_plot_dir, exist_ok=True)

    def plot_trajectories(self):
        for treatment in self.df['treatment'].unique():
            for rep in self.df['rep'].unique():
                filtered_df = self.df[(self.df['treatment'] == treatment) & (self.df['rep'] == rep)]
                num_trajectories = filtered_df['trajectory'].nunique()

                plt.figure()
                sns.lineplot(data=filtered_df, x='x', y='y', hue='trajectory', legend=False)
                plt.title(f"{treatment} {rep} trajectories")
                plt.xlabel('X axis')
                plt.ylabel('Y axis')
                plt.xlim(0, 1280)
                plt.ylim(0, 720)
                plt.annotate(f"Trajectories: {num_trajectories}", xy=(250, 600), fontsize=12, color='black')
                plt.gca().set_aspect('equal', adjustable='box')

                filename = f"{treatment}_{rep}_trajectories.pdf"
                plt.savefig(os.path.join(self.output_plot_dir, filename))
                plt.close()

    def plot_detections_per_frame(self):
        units_calculator = TimeUnitsCreator(self.df, self.config['analyse_output'].get('fps', None))
        self.df = units_calculator()
        repetitions = ["rep1", "rep2", "rep3"]
        
        for rep in repetitions:
            for treatment in ['cnt', 'b2']:
                filtered_df = self.df[(self.df['rep'] == rep) & (self.df['treatment'] == treatment)]
                plt.figure()
                sns.barplot(data=filtered_df, x='time_units', y='detections', hue='detections', palette='gray')
                plt.title(f"{treatment} {rep} detections per frame")
                plt.xlabel('Minutes')
                plt.ylabel('Detections')
                plt.xlim(0, 10)
                plt.legend(title='Detections')

                filename = f"{treatment}_{rep}.pdf"
                plt.savefig(os.path.join(self.output_plot_dir, filename))
                plt.close()
