import os

import argparse
from src.data_loader import YOLOv8DataLoader
from src.data_processor import YOLOv8DataProcessor
from src.data_visualizer import YOLOv8DataVisualizer
from src.common import Saver


def main(args):
    loader = YOLOv8DataLoader(args.labels_dir)

    loader.load_data(args.samples)
    tracking_data = loader.get_data()
    processor = YOLOv8DataProcessor(tracking_data)
    new_tracking_data = processor.sort_and_reassign_trajectories()
    Saver.check_exist(os.path.dirname(args.tracking_output_path))
    Saver.save_to_csv(new_tracking_data, args.tracking_output_path)
    saver = Saver(new_tracking_data)
    saver.save_sum_of_traj(args.general_visits_output)
    visualizer = YOLOv8DataVisualizer(tracking_data)
    visualizer.plot_x_y_by_trajectory(args.plots_output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YOLOv8 Data Processing and Visualization"
    )
    parser.add_argument(
        "--labels_dir", type=str, required=True, help="Directory containing label files"
    )
    parser.add_argument(
        "--tracking_output_path",
        type=str,
        required=True,
        help="Path to save the tracking data CSV file",
    )
    parser.add_argument(
        "--general_visits_output",
        type=str,
        default=True,
        help="Path to save the general visits CSV file",
    )
    parser.add_argument(
        "--plots_output",
        type=str,
        required=False,
        help="Directory to save the trajectory plots",
        default=None,
    )

    parser.add_argument("--samples", type=int, required=False, default=100, help="Number of samples")

    args = parser.parse_args()
    main(args)
