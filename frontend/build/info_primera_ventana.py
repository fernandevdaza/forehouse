from pathlib import Path
from tkinter import Toplevel, Canvas, PhotoImage, Button
from PIL import Image, ImageTk
from graficos.a import create_graph
from graficos.b import create_comparative_graph, df1
from graficos.c import create_ranking_graph

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_and_resize_image(image_path: Path, size: tuple[int, int]) -> PhotoImage:
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def abrir_info(root, data, data_predictions):
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

    background_image_path = relative_to_assets("background_info.png")
    background_image = load_and_resize_image(background_image_path, (1400, 950))
    if background_image:
        canvas.create_image(
            0,  
            0,  
            anchor="nw",
            image=background_image
        )
        window.background_image = background_image  

    info_button_1_image_path = relative_to_assets("info_button_1.png")
    info_button_1_image = load_and_resize_image(info_button_1_image_path, (1000, 139))
    if info_button_1_image:
        window.info_button_1_image = info_button_1_image  

        prediccion_precio_button = Button(
            window,
            image=info_button_1_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: create_graph(data_predictions),
            relief="flat"
        )
        prediccion_precio_button.place(x=200, y=200)
        prediccion_precio_button.image = info_button_1_image  

    # Load image for Button 2
    info_button_2_image_path = relative_to_assets("info_button_2.png")
    info_button_2_image = load_and_resize_image(info_button_2_image_path, (1000, 139))
    if info_button_2_image:
        window.info_button_2_image = info_button_2_image  

        sugerencia_vivienda_button = Button(
            window,
            image=info_button_2_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: create_comparative_graph(df1),
            relief="flat"
        )
        sugerencia_vivienda_button.place(x=200, y=300)
        sugerencia_vivienda_button.image = info_button_2_image  

    info_button_3_image_path = relative_to_assets("info_button_3.png")
    info_button_3_image = load_and_resize_image(info_button_3_image_path, (1000, 139))
    if info_button_3_image:
        window.info_button_3_image = info_button_3_image  

        informacion_button = Button(
            window,
            image=info_button_3_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: create_ranking_graph(data_predictions),
            relief="flat"
        )
        informacion_button.place(x=200, y=400)
        informacion_button.image = info_button_3_image  

    button_image_path = relative_to_assets("button_2.png")
    button_image = load_and_resize_image(button_image_path, (175, 56))
    if button_image:
        window.button_image = button_image  

        def on_next_button_click():
            window.destroy()
            from ventanafinal import abrir_hasta_luego  
            abrir_hasta_luego(root, data, data_predictions)

        button_1 = Button(
            window,
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=on_next_button_click,
            relief="raised"
        )
        button_1.place(x=1000.0, y=850.0)

    window.resizable(False, False)

    window.resizable(False, False)
