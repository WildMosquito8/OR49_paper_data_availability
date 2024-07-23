import os
import concurrent.futures
from src.common import Parser


class YOLOv8DataLoader:
    def __init__(self, labels_dir, parser=Parser):
        self.labels_dir = labels_dir
        self.parser_class = parser
        self.tracking_data = []
        self.malformed_lines_count = 0

    def load_data(self, samples):
        txt_files = [f for f in os.listdir(self.labels_dir) if f.endswith(".txt")]
        if samples:
            txt_files = txt_files[:samples]

        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(self.process_file, filename) for filename in txt_files
            ]
            for future in concurrent.futures.as_completed(futures):
                data, malformed_count = future.result()
                self.tracking_data.extend(data)
                self.malformed_lines_count += malformed_count

        print(f"Number of malformed lines skipped: {self.malformed_lines_count}")

    def process_file(self, filename):
        parser = self.parser_class()
        treatment, rep, frame = self.extract_treatment_rep_frame(filename)
        file_path = os.path.join(self.labels_dir, filename)
        parser.parse_file(file_path, treatment, rep, frame)
        return parser.get_data(), parser.malformed_lines_count

    def extract_treatment_rep_frame(self, filename):
        parts = filename.split("_")
        treatment = parts[0]
        rep = parts[1]
        frame = parts[2].split(".")[0]
        return treatment, rep, frame

    def get_data(self):
        return self.tracking_data
