
# Mosquito Detection and Analysis

This project provides resources and tools related to our research "A conserved odorant receptor underpins borneol-mediated repellency in culicine mosquitoes". The repository includes our YOLOv8 custom model weights, code for data collection and analysis, and sample data for experimentation.

## Repository Contents

- **YOLOv8 Model Weights**: A compressed folder custom-trained YOLOv8 model specifically designed to detect mosquitoes.
- **Code**:
  - **Python**: Scripts used to gather YOLO output.
  - **R**: Scripts used to analyze the gathered data.
- **Video Sample**: A 15-second video from the experiment, provided to test the model.
- **YOLOv8 Output**: A compressed folder containing all `.txt` files of the output.

## Setup Instructions

### Requirements

- Python 3.10.12
- R 4.0.2
- Ultralytics 8.0.228
- Other dependencies as listed in `requirements.txt` and `R_packages.txt`

### Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   \`\`\`

2. Install Python dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. Install R dependencies:
   \`\`\`R
   install.packages("dependencies from R_packages.txt")
   \`\`\`

4. Ensure YOLOv8 is installed and properly configured. https://github.com/ultralytics/ultralytics

## Usage

### Running the YOLOv8 Model

1. Place "Video sample.mp4" file in the `input` directory.
2. Run the YOLOv8 model using the provided weights:
   
'yolo track model=model/weights/best.pt source=/path/Video_sample.mp4 save_txt=true name=output conf=0.5 iou=0.5'
   

### Analyzing the Data

1. Use the provided R scripts to analyze the YOLOv8 output:
   \`\`\`R
   source("analyze_data.R")
   \`\`\`

## Sample Data

A sample video from the experiment is provided in the `sample_data` directory. You can use this video to test the YOLOv8 model and verify its functionality.

## Contributing

We welcome contributions to improve this project. Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or inquiries, please contact us at [your.email@example.com](mailto:your.email@example.com).
