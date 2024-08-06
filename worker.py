import argparse
from src.process_data import data_process_runner
from src.analyze_data import analyze_runner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 Data Processing")
    parser.add_argument("--config_path", type=str, required=True, help="Path to the JSON configuration file")
    args = parser.parse_args()
    data_process_runner.run(args)