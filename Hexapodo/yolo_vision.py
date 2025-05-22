import torch
import cv2
import matplotlib.pyplot as plt


# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=False)  # 'yolov5s' es el modelo pequeño

# Cargar imagen
image_path = '/home/lassy/MasterUGR/SC/Hexapodo/botellas2.jpg'  # Cambia esto por la ruta a tu imagen
img = cv2.imread(image_path)
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
    mejor = detecciones_filtradas.loc[detecciones_filtradas['confidence'].idxmax()]
    print("Mejor detección de tipo '{}':".format(clase_deseada))
    print(mejor)
    #mejor = detecciones_filtradas.loc[detecciones_filtradas['confidence'].idxmax()]

    # Extraer bounding box y convertir a int
    xmin = int(mejor['xmin'])
    ymin = int(mejor['ymin'])
    xmax = int(mejor['xmax'])
    ymax = int(mejor['ymax'])
    conf = mejor['confidence']
    label = f"{mejor['name']} {conf:.2f}"

    # Dibujar bounding box
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    #img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Guardar imagen en disco
    output_path = '/home/lassy/MasterUGR/SC/Hexapodo/mejor_deteccion.jpg'
    cv2.imwrite(output_path, img)
    print(f"Imagen guardada en: {output_path}")

else:
    print(f"No se detectaron objetos de tipo '{clase_deseada}'")

