import tensorflow as tf
import numpy as np
import cv2
import tensorflow_hub as hub

# Cargar el modelo preentrenado (SSD MobileNet) desde TensorFlow Hub
MODEL_URL = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"
detector = hub.load(MODEL_URL)

# Clases de objetos (mapeo básico con algunas clases)
category_index = {
    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
    6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
    11: 'fire hydrant', 12: 'stop sign', 13: 'parking meter', 14: 'bench',
    15: 'bird', 16: 'cat', 17: 'dog', 18: 'horse', 19: 'sheep', 20: 'cow',
    # Agregar más clases si es necesario
}

def detect_objects_in_frame(frame):
    """Detecta objetos en un fotograma utilizando el modelo cargado."""
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis,...]

    # Realizar la detección de objetos
    output_dict = detector(input_tensor)

    # Obtener los resultados de la detección
    boxes = output_dict['detection_boxes'][0].numpy()
    classes = output_dict['detection_classes'][0].numpy().astype(np.int32)
    scores = output_dict['detection_scores'][0].numpy()

    return boxes, classes, scores

# Abrir la cámara
cap = cv2.VideoCapture(0)

while True:
    # Capturar fotograma por fotograma
    ret, frame = cap.read()
    if not ret:
        print("No se pudo obtener un fotograma de la cámara.")
        break

    # Convertir la imagen de BGR a RGB (para compatibilidad con TensorFlow)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar objetos en el fotograma
    boxes, classes, scores = detect_objects_in_frame(frame_rgb)

    # Establecer un umbral de confianza para mostrar los objetos
    confidence_threshold = 0.5
    for i in range(len(boxes)):
        if scores[i] > confidence_threshold:
            ymin, xmin, ymax, xmax = boxes[i]
            class_name = category_index.get(classes[i], 'Desconocido')

            # Dibujar el cuadro delimitador
            cv2.rectangle(frame, 
                          (int(xmin * frame.shape[1]), int(ymin * frame.shape[0])),
                          (int(xmax * frame.shape[1]), int(ymax * frame.shape[0])), 
                          (0, 255, 0), 3)
            
            # Mostrar la categoría de objeto
            cv2.putText(frame, class_name, 
                        (int(xmin * frame.shape[1]), int(ymin * frame.shape[0] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Mostrar el fotograma con los objetos detectados
    cv2.imshow('Detección de Objetos en Tiempo Real', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
