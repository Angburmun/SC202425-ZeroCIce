import sys
import Ice
import io, cv2
import numpy as np
import time
import RoboInterface  # Generated from Hexapod.ice

class Client(Ice.Application):
    def run(self, args):
        # raspberry_pi_ip = "10.139.70.109" # Hardcoded IP
        if len(args) > 1:
            raspberry_pi_ip = args[1]
        else:
            # Fallback to hardcoded if no argument provided
            raspberry_pi_ip = "10.139.70.109"
            print(f"No IP address provided, using default: {raspberry_pi_ip}")
            # You might want to uncomment the below lines to make IP mandatory
            # print(f"Usage: {self.appName()} <raspberry_pi_ip_address>")
            # return 1


        communicator = self.communicator()
        hexapod_prx = None  # Initialize to None

        try:
            proxy_string = f"HexapodController:default -h {raspberry_pi_ip} -p 10000"
            base_proxy = communicator.stringToProxy(proxy_string)
            hexapod_prx = RoboInterface.HexapodControllerPrx.uncheckedCast(base_proxy)

            if not hexapod_prx:
                print(f"Invalid proxy for {proxy_string}")
                return 1

            print(f"Successfully connected to HexapodController on {raspberry_pi_ip}")
            print("\nControls:")
            print("  W - Move Forward")
            print("  S - Move Backward")
            print("  A - Strafe Left")
            print("  D - Strafe Right")
            print("  Q - Quit and Stop Robot")
            print("  C - Camera mode")
            print("\nHold down W, A, S, or D to move. Release to stop.")
            print("Press Q to exit.\n")

            # --- Keyboard Control Loop ---
            current_speed = 20  # You can adjust this speed
            moving = False

            while True:
                print("C pressed - Waiting for a picture from the robot...")
                hexapod_prx.stop()
                
                data = hexapod_prx.getSnapshot()

                nparr = np.frombuffer(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Puedes usar IMREAD_GRAYSCALE si prefieres

                # Mostrar imagen en ventana
                cv2.imshow("Imagen recibida", img)
                cv2.waitKey(0)  # Espera una tecla
                cv2.destroyAllWindows()
                time.sleep(0.05)


            # Request status before exiting (optional)
            # status = hexapod_prx.getStatus()
            # print(f"Final robot status: {status}")

        except KeyboardInterrupt:
            print("\nCtrl+C detected. Stopping robot and exiting.")
            if hexapod_prx and moving: # Check if proxy exists and was moving
                try:
                    hexapod_prx.stop()
                    print("Robot stopped.")
                except Ice.Exception as e:
                    print(f"Error stopping robot during Ctrl+C: {e}")
        except Ice.ConnectTimeoutException:
            print(f"Connection timed out to {raspberry_pi_ip}:10000. Is the server running?")
            return 1
        except Ice.ConnectionRefusedException:
            print(f"Connection refused by {raspberry_pi_ip}:10000. Is the server running and adapter active?")
            return 1
        except Ice.CommunicatorDestroyedException:
            print("Communicator destroyed, likely due to Q press or other shutdown.")
        except Ice.Exception as e:
            print(f"An Ice error occurred: {e}")
            if hexapod_prx and moving: # Try to stop robot on other Ice errors too
                 try:
                    hexapod_prx.stop()
                    print("Robot stopped due to Ice error.")
                 except Ice.Exception as ie:
                    print(f"Further error stopping robot: {ie}")
            return 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            if hexapod_prx and moving: # Try to stop robot
                 try:
                    hexapod_prx.stop()
                    print("Robot stopped due to unexpected error.")
                 except Ice.Exception as ie:
                    print(f"Further error stopping robot: {ie}")
            return 1
        finally:
            if communicator:
                try:
                    if hexapod_prx and moving: # Ensure stop if loop exited unexpectedly
                        print("Ensuring robot is stopped in finally block.")
                        # This might be problematic if the communicator is already shutting down
                        # hexapod_prx.stop()
                    communicator.destroy()
                    print("Communicator destroyed.")
                except Ice.Exception as e:
                    print(f"Error destroying communicator: {e}")
        return 0

if __name__ == '__main__':
    app = Client()
    # Ensure that Ice.Application.main() is called correctly
    # sys.exit(app.main(sys.argv, "config.client")) # Example if using a config file
    sys.exit(app.main(sys.argv))