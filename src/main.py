from analysis.data_loader import DataLoader
from analysis.plotter import Plotter
from analysis.analysis import Analyzer

def main():
    data_loader = DataLoader("data/tracking_data.csv")
    df = data_loader.load_and_prepare_data()
    
    plotter = Plotter(df)
    plotter.plot_trajectories()
    plotter.plot_detections_per_frame()

    analyzer = Analyzer(df)
    detections_per_frame = analyzer.calculate_detections_per_frame()
    print(detections_per_frame)

if __name__ == "__main__":
    main()
