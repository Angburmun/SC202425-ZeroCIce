import sys, Ice
import RoboInterface # Generated from Hexapod.ice

# Import the Freenove Hexapod control library
# (Assuming you have a library like 'freenove_hexapod_api')
# import freenove_hexapod_api

class HexapodControllerI(RoboInterface.HexapodController):
    def __init__(self):
        # Initialize your hexapod hardware/API here
        # self.hexapod = freenove_hexapod_api.Hexapod()
        # self.hexapod.initialize()
        print("HexapodController servant initialized.")
        pass

    def move(self, direction, speed, current=None):
        print(f"Server: Received move command - Direction: {direction}, Speed: {speed}")

        if direction == RoboInterface.MovementDirection.Forward:
            # Move forward in action mode 1 and gait mode 1
            for i in range(3):
                data = ['CMD_MOVE', '1', '0', '35', '10', '0']
                c.run(data)  # Run gait with specified parameters
        elif direction == RoboInterface.MovementDirection.Backward:
            # Move backward in action mode 2 and gait mode 2    
            for i in range(3):
                data = ['CMD_MOVE', '2', '0', '-35', '10', '10']
                c.run(data)  # Run gait with specified parameters
        

        pass

    def stop(self, current=None):
        print("Server: Received stop command")
        # self.hexapod.stop_movement()
        pass


class Server(Ice.Application):
    def run(self, args):
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1

        communicator = self.communicator()
        adapter_name = "HexapodAdapter"
        # Define the endpoint: "default -p 10000" means TCP/IP on port 10000
        # You can make the IP address specific e.g., "tcp -h YOUR_RASPBERRY_PI_IP -p 10000"
        adapter = communicator.createObjectAdapterWithEndpoints(adapter_name, "tcp -h 10.139.70.109 -p 10000")

        servant = HexapodControllerI()
        proxy = adapter.add(servant, communicator.stringToIdentity("HexapodController"))

        print(f"HexapodController servant active with proxy: {proxy}")
        adapter.activate()
        print(f"Server started on port 10000. Waiting for connections...")
        communicator.waitForShutdown()
        return 0

if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
