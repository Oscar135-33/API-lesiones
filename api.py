from flask import Flask, request, jsonify 
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        model = tf.keras.models.load_model("modelo_lesiones.keras")
        data = request.get_json()
        input_data = np.array(data["input"])
        predictions = model.predict(input_data)
        return jsonify({"prediction": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta raíz para verificación de Render
@app.route("/")
def health_check():
    return "La API está corriendo correctamente"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port)
