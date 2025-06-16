import sys, Ice
import RoboInterface  # Asegúrate de que Hexapod.ice esté compilado
import cv2

class HexapodControllerDummy(RoboInterface.HexapodController):
    def __init__(self):
        print("HexapodController dummy initialized.")

    def move(self, direction, speed, current=None):
        print(f"Dummy Server: Received move command - Direction: {direction}, Speed: {speed}")
        # No hace nada

    # def getSnapshot(self, current=None):
    #     try:
    #         filename = "lenna.jpg"
    #         print(f"Dummy Server: Reading {filename} from disk...")
    #         with open(filename, "rb") as f:
    #             image_data = f.read()
    #         print(f"Dummy Server: Loaded {len(image_data)} bytes from {filename}")
    #         return image_data
    #     except Exception as e:
    #         print(f"Error reading '{filename}': {e}")
    #         return b''  # Devuelve vacío si hay error

    def getSnapshot(self, current=None):
        try:
            cap = cv2.VideoCapture(0)
            _, frame = cap.read()
            cap.release()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] 
            _, encoded_image_array = cv2.imencode('.jpg', frame, encode_param)
            image_data = encoded_image_array.tobytes()
            print(f"Dummy Server: Captured image of size {len(image_data)} bytes")
            return image_data
        except Exception as e:
            print(f"Error capturing image from camera: {e}")
            return b''


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
        print("Dummy server started on default port. Waiting for connections...")
        communicator.waitForShutdown()
        return 0

if __name__ == '__main__':
    app = DummyServer()
    sys.exit(app.main(sys.argv, "config.server")) # if using a config file
    # sys.exit(app.main(sys.argv))
