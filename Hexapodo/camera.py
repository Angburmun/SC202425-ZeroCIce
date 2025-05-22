from picamera2 import Picamera2
from picamera2.previews.null_preview import NullPreview # Import NullPreview

picam2 = None  # Initialize picam2 to None for robust cleanup
try:
    print("Initializing Picamera2...")
    picam2 = Picamera2()

    # If you don't want any preview window to show up:
    print("Starting with NullPreview...")
    picam2.start_preview(NullPreview())

    # Configure the camera (optional, start_and_capture_file can use defaults)
    # You might want to create a specific configuration for still captures
    config = picam2.create_still_configuration()
    picam2.configure(config)
    print("Camera configured for still capture.")

    # This method will:
    # 1. Start the camera (if not already started by start_preview, though preview implicitly starts some things)
    # 2. Perform the capture
    # 3. Stop the camera
    # The preview setting (NullPreview) will be respected.
    output_file = "image2.jpg"
    print(f"Starting camera and capturing to {output_file}...")
    picam2.start_and_capture_file(output_file)
    print(f"Image saved as {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if picam2:
        # Although start_and_capture_file stops the camera,
        # explicitly stopping the preview (if started) and closing is good practice.
        print("Stopping preview (if active)...")
        picam2.stop_preview()
        print("Closing camera...")
        picam2.close()
        print("Picamera2 resources released.")