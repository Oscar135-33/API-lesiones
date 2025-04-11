import serial
import time
import tkinter as tk
import subprocess

# Configurar el puerto serie
ser = serial.Serial('/dev/ttyACM0', 9600)  
time.sleep(2)  

# Definir los rangos de BPM considerados normales
BPM_MIN = 60  # Límite inferior normal
BPM_MAX = 100  # Límite superior normal

def return_to_main():
    root.destroy()  # Cerrar la ventana principal
    subprocess.Popen([r"/usr/bin/python", "main.py"])  # Ejecutar main.py

def update_bpm():
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip() 
        if "BPM =" not in line:
            # Separar los valores usando la coma como delimitador
            values = line.split(',')
            if len(values) == 3: 
                bpm = int(values[2])  
                bpm_label.config(text=f"BPM: {bpm}")  

                # Verificar si los BPM están fuera del rango normal
                if bpm < BPM_MIN:
                    recommendation_label.config(text="BPM bajo. Intenta descansar o consultar a un médico.")
                elif bpm > BPM_MAX:
                    recommendation_label.config(text="BPM alto. Relájate y respira profundamente.")
                else:
                    recommendation_label.config(text="BPM dentro del rango normal.") 
    except Exception as e:
        print(f"Error al leer del puerto serie: {e}")

    root.after(1, update_bpm)  

root = tk.Tk()
root.title("Monitoreo de BPM")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

bpm_label = tk.Label(frame, text="Esperando datos de BPM...", font=("Helvetica", 40))
bpm_label.place(relx=0.5, rely=0.4, anchor="center")

recommendation_label = tk.Label(frame, text="", font=("Helvetica", 20))
recommendation_label.place(relx=0.5, rely=0.6, anchor="center") 

regresar_button = tk.Button(root, text="Regresar", font=("Helvetica", 20), command=return_to_main)
regresar_button.pack(side="bottom", pady=20)  # Colocar el botón abajo

update_bpm()

# Ejecutar el bucle principal
root.mainloop()

# Cerrar el puerto serie al finalizar
ser.close()
