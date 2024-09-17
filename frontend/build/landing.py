from pathlib import Path
from tkinter import Tk, Toplevel, Canvas, PhotoImage, Button
from PIL import Image, ImageTk
from utils.get_data import get_data
from utils.get_data import get_data_prediction
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

def abrir_bienvenido(root, data, data_predictions):
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
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    background_image_path = relative_to_assets("background.png")
    background_image = load_and_resize_image(background_image_path, (1400, 950))
    if background_image:
        canvas.create_image(
            0,  
            0,  
            anchor="nw",
            image=background_image
        )
        window.background_image = background_image

    button_image_path = relative_to_assets("button_1.png")
    button_image = load_and_resize_image(button_image_path, (80, 80))
    if button_image:
        def on_button_click():
            window.destroy()
            from main_menu import abrir_main
            abrir_main(root, data, data_predictions)  

        button_1 = Button(
            window,
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=on_button_click,
            relief="flat"
        )
        button_1.place(x=595.0, y=580.0)
        button_1.image = button_image  

    window.resizable(False, False)

async def main():
    data = await get_data()
    data_predictions = await get_data_prediction()
    root = Tk()
    root.withdraw()
    abrir_bienvenido(root, data, data_predictions)
    root.mainloop()

if __name__ == "__main__":
    asyncio.run(main())