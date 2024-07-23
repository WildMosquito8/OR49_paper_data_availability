import matplotlib.pyplot as plt
import os
import pandas as pd


class YOLOv8DataVisualizer:
    def __init__(self, tracking_data):
        self.tracking_data = pd.DataFrame(tracking_data)

    def plot_x_y_by_trajectory(self, output_dir=None):
        for treatment in self.tracking_data["treatment"].unique():
            subset_treatment = self.tracking_data[
                self.tracking_data["treatment"] == treatment
            ]
            plt.figure(figsize=(10, 6))
            for trajectory in subset_treatment["trajectory"].unique():
                subset_trajectory = subset_treatment[
                    subset_treatment["trajectory"] == trajectory
                ]
                plt.plot(
                    subset_trajectory["x"],
                    subset_trajectory["y"],
                    marker="o",
                    linestyle="",
                    alpha=0.2,
                )
            plt.title(f"Treatment: {treatment}")
            plt.xlabel("X Coordinate")
            plt.ylabel("Y Coordinate")
            plt.grid(True)
            if output_dir:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                plt.savefig(os.path.join(output_dir, f"{treatment}_trajectories.png"))
            plt.show()
