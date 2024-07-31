import flet as ft
from PIL import Image
from QR_create import QR_format
import os

# Lista de usuarios y contraseñas (para un ejemplo simple)
users = {"user": "pass"}

def main(page: ft.Page):
    destination_folder = "uploaded_images"
    def login(e):
        user = username.value
        pw = password.value
        if user in users and users[user] == pw:
            login_view.visible = False
            app_view.visible = True
            page.update()
        else:
            login_error.text = "Invalid username or password"
            page.update()

    def submit_data(e):
        link = link_input.value
        if image_picker.result and len(image_picker.result.files) > 0:
            image_file = image_picker.result.files[0]
            image_path = os.path.join("uploaded_images", image_file.name)
            image_picker.save_file(image_file, image_path)
            QR_format(image_path)
            
            process_data(link, image_path)
        else:
            print("No image selected")
    # Función para manejar la carga de archivos
    def on_files_picked(e: ft.FilePickerResultEvent):
        print(e.files)
        if e.files:
            file_names = [f.name for f in e.files]
            for f in e.files:
                save_path = os.path.join(destination_folder, f.name)
                print(f"path{save_path}")
                print(f"f: {f}")
                with open(f.path, "rb") as archivo:
                    with open(save_path, "wb") as archivo_destino:
                        archivo_destino.write(archivo.read())
            page.update()


    def process_data(link, image_path):
        # Aquí defines tu función para procesar los datos
        print(f"Link: {link}")
        print(f"Image Path: {image_path}")

        # Puedes usar Pillow para abrir y procesar la imagen si es necesario
        with Image.open(image_path) as img:
            img.show()

    # Crear una carpeta para guardar imágenes si no existe
    if not os.path.exists("uploaded_images"):
        os.makedirs("uploaded_images")

    # Login view
    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    login_button = ft.ElevatedButton(text="Login", on_click=login)
    login_error = ft.Text()

    login_view = ft.Column([
        username,
        password,
        login_button,
        login_error
    ])

    # App view
    link_input = ft.TextField(label="Enter link")
    image_picker = ft.FilePicker(on_result=on_files_picked)
    pick_files_button = ft.ElevatedButton(icon=ft.icons.UPLOAD_FILE, text="File", on_click=lambda _: image_picker.pick_files(allow_multiple=True))
    submit_button = ft.ElevatedButton(text="Submit", on_click=submit_data)

    app_view = ft.Column([
        link_input,
        pick_files_button,
        submit_button,
        image_picker
    ], visible=False)

    # Adding views to page
    page.add(login_view, app_view)

ft.app(target=main)
