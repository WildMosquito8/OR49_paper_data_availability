
# Mosquito detection and analysis

This project provides resources and tools related to our research "A conserved odorant receptor underpins borneol-mediated repellency in culicine mosquitoes". The repository includes our YOLOv8 custom model weights performance, code for data collection and analysis, and sample data for experimentation.

## Repository contents

- **YOLOv8 model weights**: Please contact us to get the weights.
- **Code**:
  - **Python**: Scripts used to gather YOLO output.
  - **R**: Scripts used to analyze the gathered data.
- **Video sample**: A 10-second video from the experiment, provided as an example of the input and output video.
- **YOLOv8 output**: A compressed folder containing all `.txt` files of the output.

## Setup instructions

### Requirements

- Python 3.10.12
- R 4.0.2
- Ultralytics 8.0.228
- Other dependencies as listed in `requirements.txt` and `R_packages.txt`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WildMosquito8/OR49_paper_data_avaliability.git
   cd your-repo
   ```

2. Install Python dependencies:
   ```python
   pip install -r requirements.txt
   ```

3. Install R dependencies:
   ```R
   install.packages("R_packages.txt")
   ```

4. Ensure YOLOv8 is installed and properly configured. https://github.com/ultralytics/ultralytics

## Usage

## Sample data

A sample video from the experiment with detections is provided in data -> sample_data.

### Running the YOLOv8 model

2. We Ran the YOLOv8 model using the provided weights:

```bash
yolo track model=model/weights/best.pt source=/path/Video_sample.mp4 save_txt=true name=output conf=0.5 iou=0.5
```   

### Analyzing the data

1. Use the provided Jupyternotebook to analyze the Yolov8 output:
   
   'Processing_and_analysis_YOLOv8.ipynb'
   
3. Use the provided R scripts to analyze the .csv files in data -> input:
  ```r
  Normalized_landing_git.R
  Distance_comparison_git.R
  Duration_comparison_git.R
  X_VS_Y_and_detection_over_time_git.R
  ```

For any questions or inquiries, please contact us [Evyatar Sar-shalom](mailto:evyatar.sar-shalom@huji.mai.ac.il).
