# Disclaimer
The author is not responsible for any misuse of this software. Use it at your own risk and ensure compliance with all applicable laws and regulations.

# Ethical Considerations
Use Responsibly: This software is for educational and testing purposes only. Using a keylogger to monitor someone without their explicit consent is illegal in many jurisdictions and violates privacy rights.

Transparency: Always inform and obtain consent from users before deploying this software on their systems.

Security: The ZIP file is encrypted, but ensure the password and output files are handled securely to prevent unauthorized access.

# webcamcap
This app would allow you to take a snapshot of any webcams that has been installed on the computer and then will take a snapshot one by one.  You could use windows task scheduler to run on a time interval.

# Camera Capture Script

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)

## Overview

This Python script detects available cameras connected to your system, captures a single frame from each, and saves the images as PNG files with timestamps and camera indices in the filenames. The script includes robust error handling, logging, and a modular structure for easy maintenance and extension.

Note: This project is intended for educational purposes only. Unauthorized use of webcamcap to capture webcam without consent is illegal and unethical. Ensure you have explicit permission from all parties involved before using this software.

**Author**: KPFZIPOH

## Features

- Detects all available cameras (up to 10 by default).
- Captures a single frame from each camera.
- Saves images to a configurable output directory (`C:/temp` by default) with filenames like `YYYYMMDD_HHMMSS_camX.png`.
- Logs operations and errors to a file (`camera_capture.log`) for debugging.
- Uses the DirectShow backend (`CAP_DSHOW`) for improved compatibility on Windows.
- Handles errors gracefully and ensures proper resource cleanup.

## Requirements

- **Python**: 3.6 or higher
- **OpenCV**: Install via pip:
  ```bash
  pip install opencv-python
