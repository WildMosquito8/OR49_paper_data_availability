import os
import argparse
from src.data_loader import YOLOv8DataLoader
from src.data_processor import YOLOv8DataProcessor
from src.data_visualizer import YOLOv8DataVisualizer
from src.common import Saver
from src.config import ConfigLoader  

def main(config):
    loader = YOLOv8DataLoader(config.get("labels_dir"))
    loader.load_data(config.get("samples"))
    tracking_data = loader.get_data()
    processor = YOLOv8DataProcessor(tracking_data)
    new_tracking_data = processor.sort_and_reassign_trajectories()
    Saver.check_exist(os.path.dirname(config.get("tracking_output_path")))
    Saver.save_to_csv(new_tracking_data, config.get("tracking_output_path"))
    saver = Saver(new_tracking_data)
    saver.save_sum_of_traj(config.get("general_visits_output"))
    visualizer = YOLOv8DataVisualizer(tracking_data)
    visualizer.plot_x_y_by_trajectory(config.get("plots_output"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YOLOv8 Data Processing and Visualization"
    )
    parser.add_argument(
        "--config_path",
        type=str,
        required=False,
        default="config.json",
        help="Path to the JSON configuration file"
    )

    args = parser.parse_args()

    # Load the configuration
    config_loader = ConfigLoader(args.config_path)
    config = config_loader.config
    
    main(config)
