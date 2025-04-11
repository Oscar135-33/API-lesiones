import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def cargar_y_preprocesar_datos(directorio, target_size=(224, 224), batch_size=32):
    datagen = ImageDataGenerator(rescale=1./255)
    return datagen.flow_from_directory(
        directorio,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

def dividir_datos(directorio, validation_split=0.2):
    # Función para dividir los datos si es necesario
    pass
