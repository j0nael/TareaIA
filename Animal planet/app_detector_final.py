import requests
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk


ENDPOINT = "https://frutasyverduras-prediction.cognitiveservices.azure.com/"
PREDICTION_KEY = "Frrpn47GHfC1zv3E7NRXMYe343rUAYytZVIyLEjfO5HDaUEVwqCjJQQJ99BLACYeBjFXJ3w3AAAIACOGvOWv"
PROJECT_ID = "3747d745-5295-4f65-b1f4-39684c6916f8"
ITERATION_NAME = "frutasyverduras"

ruta_imagen = None
preview_img = None

def clasificar_imagen(ruta):
    url = f"{ENDPOINT}/customvision/v3.0/Prediction/{PROJECT_ID}/classify/iterations/{ITERATION_NAME}/image"
    headers = {"Prediction-Key": PREDICTION_KEY, "Content-Type": "application/octet-stream"}

    with open(ruta, "rb") as f:
        data = f.read()

    result = requests.post(url, headers=headers, data=data).json()
    mejor = max(result["predictions"], key=lambda x: x["probability"])
    return mejor["tagName"], mejor["probability"] * 100


def seleccionar_imagen():
    global ruta_imagen, preview_img

    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
    )

    if ruta:
        ruta_imagen = ruta
        img = Image.open(ruta)
        img = img.resize((300, 300))

        preview_img = ImageTk.PhotoImage(img)
        preview_label.config(image=preview_img)

        lbl_resultado.config(text="Imagen lista, presiona CLASIFICAR.")


def ejecutar_clasificacion():
    if not ruta_imagen:
        lbl_resultado.config(text="⚠ Selecciona una imagen primero.")
        return

    lbl_resultado.config(text="Procesando...")

    nombre, prob = clasificar_imagen(ruta_imagen)

    # --- VALIDACIÓN DEL 40% ---
    if prob < 40:
        lbl_resultado.config(
            text=f"La imagen NO corresponde a una fruta o verdura."
        )
        return

    # Si pasa el 40%, mostrar resultado normal
    lbl_resultado.config(text=f"Resultado: {nombre}\nConfianza: {prob:.2f}%")


app = tk.Tk()
app.title("Detector IA de Frutas y Verduras")
app.geometry("450x650")
app.configure(bg="#0f172a")

tk.Label(app,
    text="🔍 Detector IA de Frutas y Verduras",
    font=("Segoe UI", 20, "bold"),
    fg="#38bdf8",
    bg="#0f172a"
).pack(pady=15)

preview_label = tk.Label(app, bg="#0f172a")
preview_label.pack(pady=10)

btn_seleccionar = ttk.Button(app, text="📁 Seleccionar Imagen", command=seleccionar_imagen)
btn_seleccionar.pack(pady=10)

btn_clasificar = ttk.Button(app, text="🤖 Clasificar Imagen", command=ejecutar_clasificacion)
btn_clasificar.pack(pady=10)

lbl_resultado = tk.Label(app,
    text="Selecciona una imagen para comenzar",
    font=("Segoe UI", 14),
    fg="#e2e8f0",
    bg="#0f172a"
)
lbl_resultado.pack(pady=20)

app.mainloop()
