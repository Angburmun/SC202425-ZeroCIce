import os, io, sys, Ice
import RoboInterface  # Asegúrate de que Hexapod.ice esté compilado

class HexapodControllerDummy(RoboInterface.HexapodController):
    def __init__(self):
        print("HexapodController dummy initialized.")

    def move(self, direction, speed, current=None):
        print(f"Dummy Server: Received move command - Direction: {direction}, Speed: {speed}")
        # No hace nada

    def getSnapshot(self, current=None):
        try:
            print("Dummy Server: Reading 'lenna.jpg' from disk...")
            with open("lenna.jpg", "rb") as f:
                image_data = f.read()
            print(f"Dummy Server: Loaded {len(image_data)} bytes from lenna.jpg")
            return image_data
        except Exception as e:
            print(f"Error reading 'lenna.jpg': {e}")
            return b''  # Devuelve vacío si hay error

    def stop(self, current=None):
        print("Dummy Server: Received stop command")
        # No hace nada

class DummyServer(Ice.Application):
    def run(self, args):
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1

        communicator = self.communicator()
        adapter_name = "HexapodAdapter"

        # Without IceDiscovery:
        # Define the endpoint: "default -p 10000" means TCP/IP on port 10000
        # You can make the IP address specific e.g., "tcp -h YOUR_RASPBERRY_PI_IP -p 10000"
        # adapter = communicator.createObjectAdapterWithEndpoints(adapter_name, "default -p 10000")

        adapter = communicator.createObjectAdapter(adapter_name)


        servant = HexapodControllerDummy()
        proxy = adapter.add(servant, communicator.stringToIdentity("HexapodController"))

        print(f"HexapodController dummy active with proxy: {proxy}")
        adapter.activate()
        print("Dummy server started on port 10000. Waiting for connections...")
        communicator.waitForShutdown()
        return 0

if __name__ == '__main__':
    app = DummyServer()
    sys.exit(app.main(sys.argv))
