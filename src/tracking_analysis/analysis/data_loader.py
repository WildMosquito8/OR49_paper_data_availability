import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_and_prepare_data(self):
        df = pd.read_csv(self.file_path)
        df = df.sort_values(by='frame')
        df['treatment'] = pd.Categorical(df['treatment'], categories=['cnt', 'b2'])
        df['x'] = df['x'] * 1280
        df['y'] = df['y'] * 720
        return df
