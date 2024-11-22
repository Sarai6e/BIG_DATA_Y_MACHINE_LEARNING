import cv2
import numpy as np
import tensorflow as tf
import os
import tarfile
import urllib.request

# Ruta para almacenar el modelo y etiquetas
MODEL_DIR = "ssd_mobilenet_v2_coco"
MODEL_PATH = os.path.join(MODEL_DIR, "saved_model")
LABEL_MAP_PATH ="C:\\Users\\SOPORTE\\Downloads\\BIG_DATA_Y_MACHINE_LEARNING\\22-11-24\\reconosimiento de objetos\\mscoco_label_map.pbtxt"

# URL del modelo preentrenado
MODEL_URL = "http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz"

# Función para descargar y extraer el modelo
def download_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    
    print("Descargando el modelo...")
    model_tar = os.path.join(MODEL_DIR, "model.tar.gz")
    urllib.request.urlretrieve(MODEL_URL, model_tar)
    
    print("Extrayendo el modelo...")
    with tarfile.open(model_tar, "r:gz") as tar:
        tar.extractall(MODEL_DIR)
    
    # Mover el modelo a la ruta esperada
    extracted_dir = os.path.join(MODEL_DIR, "ssd_mobilenet_v2_coco_2018_03_29", "saved_model")
    if os.path.exists(extracted_dir):
        os.rename(extracted_dir, MODEL_PATH)
    
    # Limpiar archivos temporales
    os.remove(model_tar)
    print("Modelo descargado y configurado correctamente.")

# Verificar y descargar el modelo si no existe
if not os.path.exists(MODEL_PATH):
    download_model()

# Verificar la existencia del archivo de etiquetas y permisos
if not os.path.exists(LABEL_MAP_PATH):
    print(f"Error: El archivo de etiquetas no se encuentra en {LABEL_MAP_PATH}.")
    exit()

# Verificar permisos de lectura para el archivo de etiquetas
try:
    with open(LABEL_MAP_PATH, 'r') as f:
        print("Archivo de etiquetas accesible.")
except PermissionError:
    print(f"Error: Permiso denegado al archivo {LABEL_MAP_PATH}. Verifica los permisos.")
    exit()
except Exception as e:
    print(f"Error al acceder al archivo: {e}")
    exit()

# Cargar el modelo
print("Cargando el modelo...")
try:
    detect_fn = tf.saved_model.load(MODEL_PATH)
    print("Modelo cargado con éxito.")
    # Acceder a la función de detección
    detect_fn = detect_fn.signatures['serving_default']
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    exit()

# Función para cargar etiquetas
def load_label_map(label_map_path):
    category_index = {}
    try:
        with open(label_map_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "id" in line:
                    obj_id = int(line.split(":")[-1])
                if "display_name" in line:
                    obj_name = line.split(":")[-1].strip().replace('"', '')
                    category_index[obj_id] = obj_name
    except Exception as e:
        print(f"Error al cargar las etiquetas: {e}")
        exit()
    return category_index

# Cargar las etiquetas
category_index = load_label_map(LABEL_MAP_PATH)

# Inicializar la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

print("Iniciando detección...")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el cuadro de la cámara.")
        break

    # Preprocesar la imagen
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Realizar detección
    detections = detect_fn(input_tensor)

    # Filtrar resultados
    detection_threshold = 0.5
    scores = detections['detection_scores'].numpy()[0]
    classes = detections['detection_classes'].numpy()[0].astype(int)
    boxes = detections['detection_boxes'].numpy()[0]

    # Mostrar hasta 5 detecciones
    for i in range(min(5, len(scores))):
        if scores[i] > detection_threshold:
            box = boxes[i]
            h, w, _ = frame.shape
            ymin, xmin, ymax, xmax = box
            (start_x, start_y, end_x, end_y) = (int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h))
            label = category_index.get(classes[i], "N/A")
            confidence = int(scores[i] * 100)

            # Dibujar la caja y etiqueta
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            cv2.putText(frame, f'{label}: {confidence}%', (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar la imagen procesada
    cv2.imshow('Detección de objetos', frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
