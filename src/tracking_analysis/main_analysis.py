from src.tracking_analysis.analysis.data_loader import DataLoader
from src.tracking_analysis.analysis.plotter import Plotter
from src.tracking_analysis.analysis.analysis import Analyzer
from src.process_data.config import ConfigLoader  

def main(args):
    config_loader = ConfigLoader(args.config_path)
    config = config_loader.config
    data_loader = DataLoader(config['process_data'].get("tracking_output_path"))
    df = data_loader.load_and_prepare_data()
    
    plotter = Plotter(df, config)
    plotter.plot_trajectories()
    plotter.plot_detections_per_frame()

    analyzer = Analyzer(df)
    detections_per_frame = analyzer.calculate_detections_per_frame()
    print(detections_per_frame)

if __name__ == "__main__":
    main()
