import serial
import time
import tkinter as tk
import subprocess


# Configurar el puerto serie 
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  

def update_temperatures():
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip() 
        if "BPM =" not in line: 
            # Separar los valores usando la coma como delimitador
            values = line.split(',')
            if len(values) >= 2: 
                temp_objeto, temp_ambiente = values[0], values[1]
                temperature_label.config(text=f"Temp Objeto: {temp_objeto} °C\nTemp Ambiente: {temp_ambiente} °C")  # Actualizar etiquetas
    except Exception as e:
        print(f"Error al leer del puerto serie: {e}")

    root.after(10, update_temperatures) 


def return_to_main():
    root.destroy() 
    subprocess.Popen([r"C:\Program Files\Python312\python.exe", "main.py"]) 


root = tk.Tk()
root.title("Medir Temperatura")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

temperature_label = tk.Label(frame, text="Esperando datos...", font=("Helvetica", 40))
temperature_label.place(relx=0.5, rely=0.5, anchor="center") 

regresar_button = tk.Button(root, text="Regresar", font=("Helvetica", 20), command=return_to_main)
regresar_button.pack(side="bottom", pady=20)  

update_temperatures()
root.mainloop()
ser.close()
