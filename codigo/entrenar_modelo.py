import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Desactivar advertencias de oneDNN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Oculta mensajes de info y advertencia
import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

physical_devices = tf.config.experimental.list_physical_devices('GPU')
for device in physical_devices:
    tf.config.experimental.set_memory_growth(device, True)

# Parámetros
IMG_SIZE = 224 
BATCH_SIZE = 16  # O 8
EPOCHS = 10

# Directorios de datos

# IMPORTANTE CAMBIAR LA RUTA DE LOS DATOS PORUQE PUSIMOS UNA RUTA QUE SOLO SIRVE PARA MI LAP
# IMPORTANTE CAMBIAR LA RUTA DE LOS DATOS PORUQE PUSIMOS UNA RUTA QUE SOLO SIRVE PARA MI LAP
data_dir = 'C:/Users/Greco0110/Desktop/Arduino/ComputoIntegrado/ProyectoMediKit/datos/'
train_dir = os.path.join(data_dir, 'entrenamiento')
validation_dir = os.path.join(data_dir, 'validacion')
# IMPORTANTE CAMBIAR LA RUTA DE LOS DATOS PORUQE PUSIMOS UNA RUTA QUE SOLO SIRVE PARA MI LAP
# IMPORTANTE CAMBIAR LA RUTA DE LOS DATOS PORUQE PUSIMOS UNA RUTA QUE SOLO SIRVE PARA MI LAP


# Generador de imágenes para entrenamiento con data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,         
    width_shift_range=0.2,     
    height_shift_range=0.2,    
    shear_range=0.2,            
    zoom_range=0.2,            
    horizontal_flip=True,    
    fill_mode='nearest'       
)

# Generador de imágenes para validación (sin data augmentation, solo normalización)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'  
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'  
)

print("Generadores creados con éxito.")

# Definir el modelo utilizando MobileNetV2
base_model = tf.keras.applications.MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
base_model.trainable = False  # Congelar la base para usarla como extractor de características

# Añadir capas personalizadas
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(train_generator.class_indices), activation='softmax')  
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',  
              metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

print("Modelo entrenado con éxito.")

# Guardar el modelo
model.save('modelo_lesiones.keras')
