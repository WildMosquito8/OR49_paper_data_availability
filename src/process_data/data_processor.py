import pandas as pd


class YOLOv8DataProcessor:
    def __init__(self, tracking_data):
        self.tracking_data = pd.DataFrame(tracking_data)

    def sort_and_reassign_trajectories(self):
        new_tracking_data = []
        for treatment in self.tracking_data["treatment"].unique():
            treatment_df = self.tracking_data[
                self.tracking_data["treatment"] == treatment
            ]
            rep_trajectories = {}
            for rep in treatment_df["rep"].unique():
                rep_df = treatment_df[treatment_df["rep"] == rep]
                rep_trajectories[rep] = sorted(rep_df["trajectory"].unique())
            global_trajectory = 1
            trajectory_mapping = {}
            for rep in sorted(rep_trajectories.keys()):
                for trajectory in rep_trajectories[rep]:
                    if trajectory not in trajectory_mapping:
                        trajectory_mapping[trajectory] = global_trajectory
                        global_trajectory += 1
            for _, row in treatment_df.iterrows():
                row["trajectory"] = trajectory_mapping[row["trajectory"]]
                new_tracking_data.append(row)
        return new_tracking_data

