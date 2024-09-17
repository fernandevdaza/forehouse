import sys
from pathlib import Path
from tkinter import Tk, Toplevel, Canvas, Button
from PIL import Image, ImageTk

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def load_and_resize_image(image_path: Path, size: tuple[int, int]) -> ImageTk.PhotoImage:
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading or resizing image {image_path}: {e}")
        return None

def abrir_hasta_luego(root, data, data_predictions):
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

    imagenfinal_image_path = relative_to_assets("imagenfinal.png")
    background_image = load_and_resize_image(imagenfinal_image_path, (1400, 950))
    if background_image:
        canvas.create_image(0, 0, anchor="nw", image=background_image)
        window.background_image = background_image  

    button_image_path = relative_to_assets("button5.png")
    button_image1 = load_and_resize_image(button_image_path, (250, 70))
    if button_image1:
        def on_button5_click():
            from main import abrir_main  
            window.destroy()
            abrir_main(root, data, data_predictions)

        button5 = Button(
            window,
            image=button_image1,
            borderwidth=0,
            highlightthickness=0,
            command=on_button5_click,
            relief="flat"
        )
        button5.place(x=100, y=750)
        button5.image = button_image1  

    button_image_path = relative_to_assets("button6.png")
    button_image2 = load_and_resize_image(button_image_path, (250, 70))
    if button_image2:
        def on_button6_click():
            window.destroy()
            root.destroy()  
            sys.exit()

        button6 = Button(
            window,
            image=button_image2,
            borderwidth=0,
            highlightthickness=0,
            command=on_button6_click,
            relief="flat"
        )
        button6.place(x=1050, y=750)
        button6.image = button_image2  

    window.resizable(False, False)

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    abrir_hasta_luego(root)
    root.mainloop()
