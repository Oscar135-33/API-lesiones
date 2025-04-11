import tkinter as tk
import subprocess

def run_script(script_name):
    subprocess.run(["/home/yomero/Desktop/codigo/venv/bin/python", script_name])

root = tk.Tk()
root.title("Ventana a Pantalla Completa")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

button1 = tk.Button(root, text="Detectar Herida", command=lambda: run_script("predecir_lesion.py"))
button1.pack(pady=20)

button2 = tk.Button(root, text="Medir la Temperatura Corporal", command=lambda: run_script("medirTemperatura.py"))
button2.pack(pady=20)

button3 = tk.Button(root, text="Medir la Presión Arterial", command=lambda: run_script("medirPresion.py"))
button3.pack(pady=20)

close_button = tk.Button(root, text="Cerrar", command=root.destroy)
close_button.pack(pady=20)

root.mainloop()
