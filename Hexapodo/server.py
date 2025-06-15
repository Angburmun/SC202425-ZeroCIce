import sys, os, Ice, io
import RoboInterface # Generated from Hexapod.ice
from picamera2 import Picamera2
from picamera2.previews.null_preview import NullPreview
from control import Control

# Import the Freenove Hexapod control library
# (Assuming you have a library like 'freenove_hexapod_api')
# import freenove_hexapod_api

class HexapodControllerI(RoboInterface.HexapodController):
    def __init__(self):
        # Initialize your hexapod hardware/API here
        # self.hexapod = freenove_hexapod_api.Hexapod()
        # self.hexapod.initialize()
        print("HexapodController servant initialized.")
        self.c = Control()
        pass

    def move(self, direction, speed, current=None):
        print(f"Server: Received move command - Direction: {direction}, Speed: {speed}")
        steps = 1
        
        if direction == RoboInterface.MovementDirection.FORWARD:
            for i in range(steps):
                data = ['CMD_MOVE', '1', '0', '35', speed, '0']
                self.c.run(data)
        elif direction == RoboInterface.MovementDirection.BACKWARD:
            for i in range(steps):
                data = ['CMD_MOVE', '1', '0', '-35', speed, '0']
                self.c.run(data)
        elif direction == RoboInterface.MovementDirection.LEFT:
            for i in range(steps):
                data = ['CMD_MOVE', '1', '-35', '0', speed, '0']
                self.c.run(data)
        elif direction == RoboInterface.MovementDirection.RIGHT:
            for i in range(steps):
                data = ['CMD_MOVE', '1', '35', '0', speed, '0']
                self.c.run(data)
        elif direction == RoboInterface.MovementDirection.TURN_LEFT:
            for i in range(steps):
                data = ['CMD_MOVE', '1', '0', '0', speed, '-20']
                self.c.run(data)
        elif direction == RoboInterface.MovementDirection.TURN_RIGHT:
            for i in range(steps):
                data = ['CMD_MOVE', '1', '0', '0', speed, '20']
                self.c.run(data)        
        return

    def getSnapshot():
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

            # 1. Option: save directly to a BytesIO object
            # data = io.BytesIO()
            # print(f"Starting camera and capturing image...")
            # picam2.start_and_capture_file(data, format='jpeg')
            # print(f"Image saved")
            # return data.getvalue()

            # 2. Option: save as file and than load bytes
            temp_file_path = "temp_snapshot.jpeg"
            picam2.start_and_capture_file(temp_file_path, format='jpeg')
            with open(temp_file_path, "rb") as f:
                data = f.read()
            os.remove(temp_file_path)

            return data

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

        
    def stop(self, current=None):
        print("Server: Received stop command")
        data = ['CMD_MOVE', '1', '0', '0', '0', '0']
        self.c.run(data)
        # self.hexapod.stop_movement()
        pass


class Server(Ice.Application):
    def run(self, args):
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1

        communicator = self.communicator()
        adapter_name = "HexapodAdapter"

        # Without IceDiscovery:
        # Define the endpoint: "default -p 10000" means TCP/IP on port 10000
        # You can make the IP address specific e.g., "tcp -h YOUR_RASPBERRY_PI_IP -p 10000"
        #adapter = communicator.createObjectAdapterWithEndpoints(adapter_name, "tcp -h 10.139.70.109 -p 10000")

        adapter = communicator.createObjectAdapter(adapter_name)

        servant = HexapodControllerI()
        proxy = adapter.add(servant, communicator.stringToIdentity("HexapodController"))

        print(f"HexapodController servant active with proxy: {proxy}")
        adapter.activate()
        print(f"Server started on default port. Waiting for connections...")
        communicator.waitForShutdown()
        return 0

if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
