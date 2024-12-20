# Dice detection using classic image processing techniques

This repository demonstrates the use of traditional image processing methods to detect dice in video frames and identify the number displayed on each die. The project was developed for academic purposes, focusing on the practical application of classical techniques.

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [How to Use](#how-to-use)
4. [Repository Structure](#repository-structure)
5. [Limitations](#limitations)
6. [Example Output](#example-output)
7. [License](#license)

## Overview
This project implements **classical image processing techniques** for dice detection and number recognition. The workflow involves the following steps:

1. **Frame Preprocessing**:
   - Frames are resized to reduce computational load.
   - The red color channel is extracted to leverage the dice's color properties.

2. **Dice Detection**:
   - Thresholding is applied to binarize the red channel, isolating potential dice regions.
   - Connected components analysis is used to detect regions of interest (ROI) based on their size and aspect ratio.
   - Dice positions are filtered and tracked over consecutive frames to ensure stability.

3. **Number Recognition**:
   - Regions corresponding to dice are further processed to detect dots:
     - A higher threshold is applied to isolate white dots.
     - Connected components analysis identifies individual dots based on size constraints.
   - The total number of dots for each die is calculated and tracked across frames to ensure stability.

4. **Visualization and Output**:
   - Detected dice are highlighted with bounding boxes, and the recognized numbers are overlaid on the original video.
   - The processed frames are saved as an output video.

This method relies on predefined assumptions to detect dice:
- **Dice Color**: Transparent red dice with white dots
- **Background Color**: Green

## Requirements

Before running the project, install the required dependencies:

```bash
pip install -r requirements.txt
```

**Recommended Environment:**
* Green background
* Transparent red dice with white dots

## How to Use

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Update the input-output video mappings in `video_generator.py`:
```python
video_paths_and_output = {
    "your_input_video_1.mp4": "your_output_video_1.mp4",
    "your_input_video_2.mp4": "your_output_video_2.mp4"
}
```

3. Run the script:
```bash
python video_generator.py
```

4. Output videos will be saved in the specified paths.

## Repository Structure

* `video_generator.py`: Main script to process videos
* `function.py`: Contains the `dice_number_detector` function, implementing the dice detection logic
* `requirements.txt`: Required Python libraries
* `tirada_*.mp4`: Example input videos
* `resultado_tirada_*.mp4`: Processed example output videos
* `resultado_tirada_1.gif`: GIF illustrating the output
* `Informe.pdf` & `TUIA_PDI_TP3_2023.pdf`: Report and assignment sheet

## Limitations

This approach is fine-tuned for specific conditions:
- Requires a green background to isolate dice effectively
- Only detects transparent red dice with white dots reliably
- Performance may vary with different lighting or camera angles

**Note:** This repository is intended for academic exploration and is not designed for general-purpose use cases.

## Example Output

![Dice Detection Output](resultado_tirada_1.gif)

*Example showing detected dice and their numbers overlaid on the original video*

## License

This project is licensed under the terms specified in the `LICENSE` file.
