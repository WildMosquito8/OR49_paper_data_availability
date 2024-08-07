import pandas as pd

class Analyzer:
    def __init__(self, df):
        self.df = df

    def calculate_detections_per_frame(self):
        detections_per_frame = self.df.groupby(['frame', 'treatment', 'rep']).size().reset_index(name='detections')
        detections_per_frame['min'] = detections_per_frame['frame'] / 25 / 60
        return detections_per_frame
