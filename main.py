# Author: KPFZIPOH
# Description: This script detects available cameras, captures a single frame from each,
# and saves it as a PNG file with a timestamp and camera index in the filename.
# Enhanced with error handling, logging, and configurable output directory.

import cv2
import time
import os
import logging

# Configure logging to track operations and errors
logging.basicConfig(
    filename='camera_capture.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def detect_cameras(max_cameras=10):
    """
    Detects available camera devices by attempting to open each camera index.
    
    Args:
        max_cameras (int): Maximum number of camera indices to check (default is 10).
    
    Returns:
        list: List of available camera indices.
    """
    camera_list = []
    logging.info("Starting camera detection")
    
    for i in range(max_cameras):
        try:
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Use DirectShow backend for Windows compatibility
            if cap.isOpened() and cap.read()[0]:
                camera_list.append(i)
                logging.info(f"Camera {i} detected")
            cap.release()
        except Exception as e:
            logging.error(f"Error detecting camera {i}: {str(e)}")
            break
    
    return camera_list

def capture_and_save_frame(camera_index, output_dir="C:/temp"):
    """
    Captures a single frame from the specified camera and saves it as a PNG file.
    
    Args:
        camera_index (int): Index of the camera to capture from.
        output_dir (str): Directory to save the captured image (default is C:/temp).
    
    Returns:
        bool: True if capture and save were successful, False otherwise.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"Created output directory: {output_dir}")
        except Exception as e:
            logging.error(f"Failed to create output directory {output_dir}: {str(e)}")
            return False

    # Initialize camera
    try:
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            logging.error(f"Unable to open camera {camera_index}")
            return False

        # Capture a frame
        ret, frame = cap.read()
        if not ret:
            logging.error(f"Failed to capture frame from camera {camera_index}")
            cap.release()
            return False

        # Generate filename with timestamp and camera index
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f"{timestamp}_cam{camera_index + 1}.png")
        
        # Save the frame as a PNG file
        cv2.imwrite(filename, frame)
        logging.info(f"Photo from camera {camera_index} saved to {filename}")
        
        # Release the camera
        cap.release()
        return True

    except Exception as e:
        logging.error(f"Error capturing from camera {camera_index}: {str(e)}")
        if 'cap' in locals():
            cap.release()
        return False

def main():
    """
    Main function to detect available cameras and capture a frame from each.
    """
    # Define output directory
    output_dir = "C:/temp"
    
    # Detect available cameras
    camera_list = detect_cameras()
    num_cameras = len(camera_list)
    logging.info(f"Found {num_cameras} camera(s): {camera_list}")

    if num_cameras == 0:
        logging.warning("No cameras detected. Exiting.")
        print("No cameras detected. Check connections and try again.")
        return

    # Capture a frame from each camera
    for camera_index in camera_list:
        success = capture_and_save_frame(camera_index, output_dir)
        if success:
            print(f"Successfully captured and saved frame from camera {camera_index}")
        else:
            print(f"Failed to capture frame from camera {camera_index}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
        print("Program terminated by user")
    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
