# Traffic Cone Detection

This repository contains Python code for identifying traffic cone.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/JaeyeshBalaji/Traffic-Cone-Detection.git
    cd Traffic-Cone-Detection
    ```

2. Create a virtual environment and activate it:
    - On **Linux/macOS**:
      ```sh
      python3 -m venv venv
      source venv/bin/activate
      ```
    - On **Windows**:
      ```sh
      python -m venv venv
      .\venv\Scripts\activate
      ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

 Run the traffic cone detection script:
    ```sh
    python findCone.py cone.jpg
    ```
While the script is running, you can adjust the trackbars to modify the HSV ranges for cone detection. Press q in the OpenCV window to exit the script.
