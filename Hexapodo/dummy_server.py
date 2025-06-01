import sys, Ice
import RoboInterface  # Asegúrate de que Hexapod.ice esté compilado

class HexapodControllerDummy(RoboInterface.HexapodController):
    def __init__(self):
        print("HexapodController dummy initialized.")

    def move(self, direction, speed, current=None):
        print(f"Dummy Server: Received move command - Direction: {direction}, Speed: {speed}")
        # No hace nada

    def getSnapshot(self, current=None):
        print("Dummy Server: Received getSnapshot command")
        return b''  # Devuelve un byte string vacío, válido para Ice

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
        # Define the endpoint: "default -p 10000" means TCP/IP on port 10000
        # You can make the IP address specific e.g., "tcp -h YOUR_RASPBERRY_PI_IP -p 10000"
        adapter = communicator.createObjectAdapterWithEndpoints(adapter_name, "default -p 10000")

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
