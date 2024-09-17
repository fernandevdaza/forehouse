from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button
from PIL import Image, ImageTk
from utils.get_data import get_data, get_data_prediction
from prediccion_primera_ventana import abrir_prediccion_primera_ventana
from info_primera_ventana import abrir_info
from tkinter import Toplevel
import asyncio

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def load_and_resize_image(image_path: Path, size: tuple[int, int]) -> PhotoImage:
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def abrir_main(root, data, data_predictions):
    window = Toplevel(root)
    window.geometry("1400x950")
    window.configure(bg="#EAE6E5")

    canvas = Canvas(
        window,
        bg="#EAE6E5",
        height=950,
        width=1400,
        bd=0,
        highlightthickness=0,
        relief="flat"
    )
    canvas.place(x=0, y=0)

    background_image_path = relative_to_assets("background_main.png")
    background_image = load_and_resize_image(background_image_path, (1400, 950))
    if background_image:
        canvas.create_image(
            0,  
            0,  
            anchor="nw",
            image=background_image
        )
        window.background_image = background_image  

    prediccion_precio_button_image_path = relative_to_assets("prediccion_precio_button.png")
    prediccion_precio_button_image = load_and_resize_image(prediccion_precio_button_image_path, (600, 180))
    if prediccion_precio_button_image:
        prediccion_precio_button = Button(
            window,
            image=prediccion_precio_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [window.destroy(), abrir_prediccion_primera_ventana(root, data, data_predictions)],
            relief="flat"
        )
        prediccion_precio_button.place(x=670, y=350)
        prediccion_precio_button.image = prediccion_precio_button_image  

    informacion_button_image_path = relative_to_assets("informacion_button.png")
    informacion_button_image = load_and_resize_image(informacion_button_image_path, (600, 180))
    if informacion_button_image:
        informacion_button = Button(
            window,
            image=informacion_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [window.destroy(), abrir_info(root, data, data_predictions)],
            relief="flat"
        )
        informacion_button.place(x=670, y=500)
        informacion_button.image = informacion_button_image  

    window.resizable(False, False)

def main():
    root = Tk()
    root.withdraw()  

    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(get_data())
    data_predictions = loop.run_until_complete(get_data_prediction())

    abrir_main(root, data, data_predictions)

    root.mainloop()

if __name__ == "__main__":
    main()
