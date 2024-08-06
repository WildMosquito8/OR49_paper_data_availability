import os
import argparse
from src.process_data.data_loader import YOLOv8DataLoader
from src.process_data.data_processor import YOLOv8DataProcessor
from src.process_data.data_visualizer import YOLOv8DataVisualizer
from src.process_data.common import Saver
from src.process_data.config import ConfigLoader  

def run(args):
    config_loader = ConfigLoader(args.config_path)
    config = config_loader.config
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
