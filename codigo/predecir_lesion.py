import os
import warnings
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Desactivar advertencias de oneDNN y mensajes de info/advertencia
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.filterwarnings("ignore")

# Cargar el modelo entrenado
model = tf.keras.models.load_model('modelo_lesiones.keras')

# Parámetros de la imagen
IMG_SIZE = 224  # Debe coincidir con el tamaño de entrada del modelo

# Mapear índices a nombres de clases
class_names = ['alergias', 'cortaduras', 'esguinces', 'fracturas', 'hematomas', 'no_lesiones', 'quemaduras', 'raspaduras']

# Diccionario con recomendaciones de medicamentos
recommendations = {
    'alergias': ['autoinyector', 'cetirizina', 'clorfeniramina'],
    'cortaduras': ['agua oxigenada', 'gasas', 'vendas'],
    'esguinces': ['ibuprofeno', 'paracetamol', 'vendas'],
    'fracturas': ['ibuprofeno', 'paracetamol', 'vendas'],
    'hematomas': ['ibuprofeno', 'ácido acetilsalicílico'],
    'no_lesiones': ['ningún medicamento necesario'],
    'quemaduras': ['agua oxigenada', 'vendas', 'gasas'],
    'raspaduras': ['agua oxigenada', 'gasas', 'vendas']
}


def load_and_prep_image(filename):
    img = image.load_img(filename, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión para el batch
    img_array /= 255.  # Normalizar
    return img_array

def predict_image(filename):
    img_array = load_and_prep_image(filename)
    prediction = model.predict(img_array)
    
    # Obtener la clase con la mayor probabilidad
    predicted_class = np.argmax(prediction, axis=1)[0]
    predicted_probabilities = prediction[0]
    
    # Mostrar resultados con nombres de clases
    print("Probabilidades por clase:")
    for i, prob in enumerate(predicted_probabilities):
        print(f"{class_names[i]}: {prob * 100:.2f}%")
    
    # Identificar la clase con la mayor probabilidad
    highest_probability_class = class_names[predicted_class]
    print(f"La imagen se clasifica como: {highest_probability_class}")
    
    # Mostrar recomendaciones
    print(f"Recomendaciones para {highest_probability_class}:")
    for recommendation in recommendations[highest_probability_class]:
        print(f"- {recommendation}")

def take_picture():
  
    # Definir el nombre y la ruta del archivo
    filename = "images.jpg"

    # Tomar la foto usando libcamera-still
    os.system(f"libcamera-still -o {filename} -t 10000")     # mejoraremos esto tambien

    print(f"Imagen guardada como {filename}")

    predict_image(filename)

# Ejecutar la función para capturar imagen y predecir
take_picture()

