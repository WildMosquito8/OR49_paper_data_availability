import pandas as pd

class TimeUnitsCreator:
    def __init__(self, df: pd.DataFrame, fps: int):
        self.df = df
        self.fps = fps

    def __call__(self) -> pd.DataFrame:
        self.calc_time_units()
        return self.df

    def calc_time_units(self):
        frames_per_minute = self.fps * 60
        self.df['time_units'] = self.df['frame'] // frames_per_minute
