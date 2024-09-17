from pathlib import Path
from tkinter import Toplevel, Canvas, Label, Entry, StringVar, BooleanVar, Button, OptionMenu, PhotoImage, messagebox
from PIL import Image, ImageTk
import http.client
import json

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
        print(f"Error loading image {image_path}: {e}")
        return None

def toggle_feature(feature_var, button):
    feature_var.set(not feature_var.get())
    button.config(bg="#8FCB9B" if feature_var.get() else "#CCCCCC")

def validate_numeric_input(value, var, var_type='int'):
    if value:
        try:
            if var_type == 'int':
                int(value)
            elif var_type == 'float':
                float(value)
            else:
                raise ValueError('Unknown var_type')
        except ValueError:
            messagebox.showerror("Entrada inválida", "Solo se aceptan valores numéricos.")
            var.set('')
    return True

con = http.client.HTTPSConnection("f8c2-2800-cd0-5404-af00-00-a.ngrok-free.app")

def guardar_informacion(terreno_var, construccion_var, banos_var, habitaciones_var, garaje_var,
                        barrio_var, distrito_var, window, precio_label):

    try:
        selected_district_name = distrito_var.get()
        selected_neighborhood_name = barrio_var.get()
        bedrooms = int(habitaciones_var.get())
        bathrooms = int(banos_var.get())
        garages = int(garaje_var.get())
        built_area = float(construccion_var.get())
        terrain_area = float(terreno_var.get())
        selected_neighborhood_id = window.neighborhood_name_to_id[selected_neighborhood_name]
        selected_district_id = window.district_name_to_id[selected_district_name]
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa todos los campos numéricos correctamente.")
        return

    informacion = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "garages": garages,
        "built_area": built_area,
        "terrain_area": terrain_area,
        "neighborhood_id": selected_neighborhood_id,
        "district_id": selected_district_id
    }
    print("Información guardada:", informacion)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    con.request("POST", "/predict_house_price/predict_one", body=json.dumps(informacion), headers=headers)
    res = con.getresponse()
    data = res.read()

    if res.status == 200:
        print("Server response:", data)
        response_json = json.loads(data.decode('utf-8'))
        predicted_price = response_json.get('prices', {}).get('final_predicted_price', None)
        if predicted_price is not None:
            precio_label.config(text=f"Precio Predicho: ${predicted_price:,.2f}",
                                font=("Roboto", 16, "bold"),
                                fg="#FFFFFF",
                                bg="#5c9179"
                                )
            precio_label.place(x=100, y=760)
        else:
            messagebox.showerror("Error", "No se pudo obtener el precio predicho.")
    else:
        print("Server error:", res.status, data)
        messagebox.showerror("Error", f"Error del servidor: {res.status}\n{data.decode('utf-8')}")

def abrir_prediccion_primera_ventana(root, data, data_predictions):

    window = Toplevel(root)
    window.geometry("1440x950")
    window.configure(bg="#EAE6E5")

    canvas = Canvas(
        window,
        bg="#EAE6E5",
        height=950,
        width=1440,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    detalle_image_path = relative_to_assets("detalle.png")
    detalle_image = load_and_resize_image(detalle_image_path, (550, 850))
    if detalle_image:
        canvas.create_image(325, 475, image=detalle_image)
        window.detalle_image = detalle_image  

    forehouse_image_path = relative_to_assets("forehouse.png")
    forehouse_image = load_and_resize_image(forehouse_image_path, (100, 100))
    if forehouse_image:
        canvas.create_image(1320, 75, image=forehouse_image)
        window.forehouse_image = forehouse_image  

    mapa_image_path = relative_to_assets("mapa.png")
    mapa_image = load_and_resize_image(mapa_image_path, (780, 680))
    if mapa_image:
        canvas.create_image(1010, 490, image=mapa_image)
        window.mapa_image = mapa_image  

    canvas.create_text(
        910, 110,
        text="Selecciona la ubicación de tu casa:",
        fill="#000000",
        font=("Roboto", 25)
    )

    terreno_var = StringVar()
    terreno_var.trace_add("write", lambda *args: validate_numeric_input(terreno_var.get(), terreno_var, 'float'))
    Label(window, text="Terreno (m²):", bg="#efedec", font=("Roboto", 14)).place(x=100, y=300)
    Entry(window, textvariable=terreno_var, font=("Roboto", 14), width=10).place(x=260, y=300)

    construccion_var = StringVar()
    construccion_var.trace_add("write", lambda *args: validate_numeric_input(construccion_var.get(), construccion_var, 'float'))
    Label(window, text="Construcción (m²):", bg="#efedec", font=("Roboto", 14)).place(x=100, y=350)
    Entry(window, textvariable=construccion_var, font=("Roboto", 14), width=10).place(x=260, y=350)

    banos_var = StringVar()
    banos_var.trace_add("write", lambda *args: validate_numeric_input(banos_var.get(), banos_var, 'int'))
    Label(window, text="Baños:", bg="#efedec", font=("Roboto", 14)).place(x=100, y=400)
    Entry(window, textvariable=banos_var, font=("Roboto", 14), width=5).place(x=260, y=400)

    habitaciones_var = StringVar()
    habitaciones_var.trace_add("write", lambda *args: validate_numeric_input(habitaciones_var.get(), habitaciones_var, 'int'))
    Label(window, text="Habitaciones:", bg="#efedec", font=("Roboto", 14)).place(x=100, y=450)
    Entry(window, textvariable=habitaciones_var, font=("Roboto", 14), width=5).place(x=260, y=450)

    garaje_var = StringVar()
    garaje_var.trace_add("write", lambda *args: validate_numeric_input(garaje_var.get(), garaje_var, 'int'))
    Label(window, text="Garaje:", bg="#efedec", font=("Roboto", 14)).place(x=100, y=500)
    Entry(window, textvariable=garaje_var, font=("Roboto", 14), width=5).place(x=260, y=500)

    window.district_name_to_id = {distrito['nombre']: distrito['_id'] for distrito in data if len(distrito['neighborhoods']) > 0}
    distritos = list(window.district_name_to_id.keys())

    distrito_var = StringVar(window)
    distrito_var.set(distritos[0])
    Label(window, text="Distrito:", bg="#efedec", font=("Roboto", 14)).place(x=100, y=550)
    OptionMenu(window, distrito_var, *distritos).place(x=260, y=550)

    barrio_var = StringVar(window)

    def update_neighborhoods(*args):
        selected_district_name = distrito_var.get()
        selected_district_id = window.district_name_to_id[selected_district_name]
        selected_district = next((district for district in data if district['_id'] == selected_district_id), None)
        if not selected_district:
            print("District not found")
            return

        window.neighborhood_name_to_id = {neighborhood['nombre']: neighborhood['_id'] for neighborhood in selected_district['neighborhoods']}
        barrios = list(window.neighborhood_name_to_id.keys())

        barrio_var.set(barrios[0])
        if hasattr(window, 'barrio_optionmenu'):
            window.barrio_optionmenu.destroy()
        window.barrio_optionmenu = OptionMenu(window, barrio_var, *barrios)
        window.barrio_optionmenu.place(x=260, y=600)

    update_neighborhoods()  
    distrito_var.trace_add("write", update_neighborhoods)

    Label(window, text="Barrio:", bg="#efedec", font=("Roboto", 14)).place(x=100, y=600)

    features = ["Piscina", "Amoblado", "Jardín"]
    feature_vars = [BooleanVar() for _ in features]

    for i, feature in enumerate(features):
        var = feature_vars[i]
        button_width = 11
        button_height = 2
        button = Button(window, text=feature, font=("Helvetica", 12),
                        width=button_width, height=button_height, borderwidth=0,
                        relief="flat", bg="#CCCCCC",
                        command=lambda v=var, b=None: toggle_feature(v, b))
        button.place(x=90 + (i % 3) * 180, y=650 + (i // 3) * 80)
        button.config(command=lambda v=var, b=button: toggle_feature(v, b))

    precio_label = Label(window, text="", font=("Helvetica", 20), bg="#EAE6E5", fg="green")
    precio_label.place(x=100, y=800)

    save_button_image_path = relative_to_assets("save_button.png")
    save_button_image = load_and_resize_image(save_button_image_path, (60, 60))
    if save_button_image:
        window.save_button_image = save_button_image  

        Button(window,
               image=save_button_image,
               borderwidth=0,
               highlightthickness=0,
               command=lambda: guardar_informacion(terreno_var, construccion_var, banos_var, habitaciones_var,
                                                  garaje_var, barrio_var, distrito_var, window, precio_label),
               relief="raised").place(x=485, y=740)

    # Botón siguiente
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
        button_1.place(x=1200.0, y=850.0)

    window.resizable(False, False)
