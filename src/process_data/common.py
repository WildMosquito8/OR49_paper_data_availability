import pandas as pd
import os

class Parser:
    def __init__(self):
        self.tracking_data = []
        self.malformed_lines_count = 0

    def parse_file(self, file_path, treatment, rep, frame):
        with open(file_path, "r") as file:
            for line in file:
                self.parse_line(line.strip(), treatment, rep, frame)

    def parse_line(self, line, treatment, rep, frame):
        values = line.split()
        if len(values) != 6:
            self.malformed_lines_count += 1
            return
        self.tracking_data.append(
            {
                "frame": int(frame),
                "x": float(values[1]),
                "y": float(values[2]),
                "trajectory": int(values[5]),
                "treatment": treatment,
                "rep": rep,
            }
        )

    def get_data(self):
        return self.tracking_data


class Saver:
    def __init__(self, tracking_data):
        self.tracking_data = pd.DataFrame(tracking_data)

    @staticmethod
    def check_exist(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    @staticmethod
    def save_to_csv(df, output_file_path):
        df = pd.DataFrame(df)
        df.to_csv(output_file_path, index=False)

    def save_sum_of_traj(self, output_file_path):
        movie_duration = 10
        sampling_rate = 25
        frames_per_interval = sampling_rate * 60
        num_intervals = movie_duration // 1
        intervals = pd.cut(
            self.tracking_data["frame"], bins=num_intervals, labels=False
        )
        self.tracking_data["time_interval"] = intervals
        general_visits = (
            self.tracking_data.groupby(["treatment", "time_interval", "rep"])[
                "trajectory"
            ]
            .nunique()
            .reset_index(name="counts")
        )
        general_visits.to_csv(output_file_path, index=False)
