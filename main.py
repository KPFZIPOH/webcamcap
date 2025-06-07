# Author: KPFZIPOH 
# Description: This script detects available cameras, captures frames based on user arguments,
# and saves them as PNG files with timestamps and camera indices. Supports one-time capture
# with -onetimeonly flag, or multiple captures at intervals for a specified duration.
# Enhanced with argument parsing, error handling, and logging.

import cv2
import time
import os
import logging
import argparse

# Configure logging to track operations and errors
logging.basicConfig(
    filename='camera_capture.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_arguments():
    """
    Parse command-line arguments for capture count, interval, duration, and one-time mode.
    
    Returns:
        argparse.Namespace: Parsed arguments with captures, interval, duration, and onetimeonly.
    """
    parser = argparse.ArgumentParser(description="Capture frames from cameras with configurable intervals, duration, or one-time capture.")
    parser.add_argument('-c', '--captures', type=int, default=1, help='Number of captures per interval (default: 1, ignored with -onetimeonly)')
    parser.add_argument('-i', '--interval', type=float, default=10, help='Interval between captures in seconds (default: 10, ignored with -onetimeonly)')
    parser.add_argument('-d', '--duration', type=float, default=60, help='Total duration in minutes (default: 60, ignored with -onetimeonly)')
    parser.add_argument('--onetimeonly', action='store_true', help='Capture one frame per camera and exit, ignoring other arguments')
    args = parser.parse_args()
    
    # Validate arguments (only if not in one-time mode)
    if not args.onetimeonly:
        if args.captures < 1:
            logging.error("Captures must be at least 1")
            raise ValueError("Captures must be at least 1")
        if args.interval <= 0:
            logging.error("Interval must be greater than 0")
            raise ValueError("Interval must be greater than 0")
        if args.duration <= 0:
            logging.error("Duration must be greater than 0")
            raise ValueError("Duration must be greater than 0")
    
    return args

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
    Main function to detect available cameras and capture frames based on user arguments.
    Supports one-time capture or interval-based captures.
    """
    # Parse command-line arguments
    try:
        args = parse_arguments()
        captures_per_interval = args.captures
        interval_secs = args.interval
        duration_secs = args.duration * 60  # Convert minutes to seconds
        onetimeonly = args.onetimeonly
        logging.info(f"Arguments: onetimeonly={onetimeonly}, captures={captures_per_interval}, interval={interval_secs}s, duration={args.duration}min")
    except ValueError as e:
        print(f"Invalid argument: {str(e)}")
        return

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

    # One-time capture mode
    if onetimeonly:
        logging.info("Running in one-time capture mode")
        for camera_index in camera_list:
            success = capture_and_save_frame(camera_index, output_dir)
            if success:
                print(f"Successfully captured and saved frame from camera {camera_index}")
            else:
                print(f"Failed to capture frame from camera {camera_index}")
        return

    # Interval-based capture loop
    start_time = time.time()
    while time.time() - start_time < duration_secs:
        interval_start = time.time()
        for _ in range(captures_per_interval):
            for camera_index in camera_list:
                success = capture_and_save_frame(camera_index, output_dir)
                if success:
                    print(f"Successfully captured and saved frame from camera {camera_index}")
                else:
                    print(f"Failed to capture frame from camera {camera_index}")
        
        # Wait for the next interval
        elapsed = time.time() - interval_start
        sleep_time = max(0, interval_secs - elapsed)
        try:
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            logging.info("Capture loop interrupted by user")
            print("Capture loop interrupted by user")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
        print("Program terminated by user")
    except Exception as e:
        logging.error(f"Unexpected error in main: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
