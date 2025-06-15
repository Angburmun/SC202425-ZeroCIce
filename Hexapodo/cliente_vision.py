import sys
import Ice
import io, cv2
import numpy as np
import time
import RoboInterface  # Generated from Hexapod.ice
import keyboard       # For reading keyboard input
import torch

def yolo_vision(img):
    # Cargar el modelo YOLOv5 preentrenado
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=False)  # 'yolov5s' es el modelo pequeño

    # Cargar imagen
    #image_path = '/home/lassy/MasterUGR/SC/Hexapodo/botellas2.jpg'  # Cambia esto por la ruta a tu imagen
    #img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Realizar predicción
    results = model(img_rgb)

    # Mostrar resultados
    print("--------------")
    results.print()  # Muestra por consola las detecciones
    print("--------------")

    #results.show()   # Abre una ventana con los resultados dibujados

    df = results.pandas().xyxy[0]  # Cada fila es una detección

    # Filtrar por clase deseada (ejemplo: 'person')
    clase_deseada = 'bottle'
    detecciones_filtradas = df[df['name'] == clase_deseada]

    # Obtener la detección con mayor confianza
    if not detecciones_filtradas.empty:
        # Filtrar detecciones con confianza mayor al 50%
        detecciones_filtradas = detecciones_filtradas[detecciones_filtradas['confidence'] > 0.5]

        bounding_boxes = []
        # Dibujar una caja para cada detección con confianza > 50%
        for _, fila in detecciones_filtradas.iterrows():
            xmin = int(fila['xmin'])
            ymin = int(fila['ymin'])
            xmax = int(fila['xmax'])
            ymax = int(fila['ymax'])
            conf = fila['confidence']
            label = f"{fila['name']} {conf:.2f}"

            bounding_boxes.append((xmin, ymin, xmax, ymax, label))

            # Dibujar bounding box
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        #img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # Guardar imagen en disco
        output_path = 'detecciones.jpg'
        cv2.imwrite(output_path, img)
        print(f"Imagen guardada en: {output_path}")
        return bounding_boxes

    else:
        print(f"No se detectaron objetos de tipo '{clase_deseada}'")
        return []



class Client(Ice.Application):
    def show_help(self):
        print("---------------------")
        print("\nControls:")
        print("  W - Move Forward")
        print("  S - Move Backward")
        print("  A - Strafe Left")
        print("  D - Strafe Right")
        print("  Q - Quit and Stop Robot")
        print("  C - Camera mode")
        print("\nHold down W, A, S, or D to move. Release to stop.")
        print("Press Q to exit.\n")
        return

    def run(self, args):
        # # raspberry_pi_ip = "10.139.70.109" # Hardcoded IP
        # if len(args) > 1:
        #     raspberry_pi_ip = args[1]
        # else:
        #     # Fallback to hardcoded if no argument provided
        #     raspberry_pi_ip = "10.139.70.109"
        #     print(f"No IP address provided, using default: {raspberry_pi_ip}")
        #     # You might want to uncomment the below lines to make IP mandatory
        #     # print(f"Usage: {self.appName()} <raspberry_pi_ip_address>")
        #     # return 1


        communicator = self.communicator()
        hexapod_prx = None  # Initialize to None

        try:
            # Without IceDiscovery:
            # proxy_string = f"HexapodController:default -h {raspberry_pi_ip} -p 10000"

            proxy_string = "HexapodController@HexapodAdapter"
            base_proxy = communicator.stringToProxy(proxy_string)
            hexapod_prx = RoboInterface.HexapodControllerPrx.checkedCast(base_proxy)

            if not hexapod_prx:
                print(f"Invalid proxy for {proxy_string}")
                return 1
            
            
            print(f"Successfully connected to HexapodController")

            self.show_help()  # Show controls at the start

            # --- Keyboard Control Loop ---
            current_speed = '10'  # You can adjust this speed
            moving = False

            while True:
                if keyboard.is_pressed('q'):
                    print("Q pressed, exiting...")
                    if moving: # Ensure robot is stopped if it was moving
                        print("Stopping robot before exit.")
                        hexapod_prx.stop()
                    break # Exit the loop

                new_movement = False
                if keyboard.is_pressed('w'):
                    print("W pressed - Moving Forward")
                    hexapod_prx.move(RoboInterface.MovementDirection.FOWARD, current_speed)
                    new_movement = True
                elif keyboard.is_pressed('s'):
                    print("S pressed - Moving Backward")
                    hexapod_prx.move(RoboInterface.MovementDirection.BACKWARD, current_speed)
                    new_movement = True
                elif keyboard.is_pressed('a'):
                    print("A pressed - Moving Left")
                    hexapod_prx.move(RoboInterface.MovementDirection.LEFT, current_speed)
                    new_movement = True
                elif keyboard.is_pressed('d'):
                    print("D pressed - Moving Right")
                    hexapod_prx.move(RoboInterface.MovementDirection.RIGHT, current_speed)
                    new_movement = True
                elif keyboard.is_pressed('c'):
                    print("C pressed - Waiting for a picture from the robot...")
                    
                    data = hexapod_prx.getSnapshot()

                    nparr = np.frombuffer(data, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Puedes usar IMREAD_GRAYSCALE si prefieres

                    # Mostrar imagen en ventana
                    #cv2.imshow("Imagen recibida", img)
                    #cv2.waitKey(0)  # Espera una tecla
                    #cv2.destroyAllWindows()
                    bounding_boxes = yolo_vision(img)

                    if bounding_boxes:
                        height, width, _ = img.shape
                        left_count, center_count, right_count = 0, 0, 0
                        for (xmin, ymin, xmax, ymax, label) in bounding_boxes:
                            center_x = (xmin + xmax) // 2
                            # Define thresholds
                            if center_x < width / 3:
                                left_count += 1
                            elif center_x < 2 * width / 3:
                                center_count += 1
                            else:
                                right_count += 1

                        print(f"Left: {left_count}, Center: {center_count}, Right: {right_count}")
                        if center_count == 0:
                            print("Robot should move forward.")
                            hexapod_prx.move(RoboInterface.MovementDirection.FOWARD, current_speed)
                        elif left_count == 0:
                            print("Robot should turn left.")
                            hexapod_prx.move(RoboInterface.MovementDirection.TURN_LEFT, current_speed)
                        elif right_count == 0:                              
                            print("Robot should turn right.")
                            hexapod_prx.move(RoboInterface.MovementDirection.TURN_RIGHT, current_speed)
                        else:
                            print("No clear direction found, turning right.")
                            hexapod_prx.move(RoboInterface.MovementDirection.TURN_RIGHT, current_speed)
                    else:
                        print("No bottle detected, moving forward.")
                        hexapod_prx.move(RoboInterface.MovementDirection.FOWARD, current_speed)
                            

                    self.show_help()  # Show controls again after camera mode
                
                if new_movement and not moving:
                    moving = True
                    print("Robot started moving.")
                elif not new_movement and moving:
                    print("No movement key pressed - Stopping robot.")
                    hexapod_prx.stop()
                    moving = False
                
                # Small delay to prevent overwhelming the CPU and network
                # Adjust if necessary for responsiveness
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
            print(f"Connection timed out. Is the server running?")
            return 1
        except Ice.ConnectionRefusedException:
            print(f"Connection refused. Is the server running and adapter active?")
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
                    if hexapod_prx and moving and not keyboard.is_pressed('q'): # Ensure stop if loop exited unexpectedly
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