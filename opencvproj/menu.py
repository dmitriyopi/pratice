import tkinter as tk
import os

def run_script(script_name):
    os.system(f"python {script_name}")
root = tk.Tk()
root.title("Меню")
root.geometry("400x400")
label = tk.Label(root, text="Оберіть програму", font=("Arial", 16))
label.pack(pady=10)
scripts = {
    "Зміна фону": "bg.py",
    "Розмиття": "blur.py",
    "Керування мишкою": "camera_mouse.py",
    "Малювання": "drawing.py",
    "Детектор руху": "motion_detector.py",
    "Селфі камера": "selfie_camera.py",
    "Зміна гучності": "volume_changer.py"
}
for name, script in scripts.items():
    button = tk.Button(root, text=name, width=30, height=2,command=lambda s=script: run_script(s))
    button.pack(pady=5)
exit_button = tk.Button(root, text="Вийти", width=30, height=2, command=root.quit)
exit_button.pack(pady=6)
root.mainloop()
