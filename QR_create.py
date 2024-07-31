import qrcode
from PIL import Image


def create_QR ():
    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data("https://www.figma.com/proto/X0iV0raNGN3RJQCoYf9Az3/Sancor---AP-Form?node-id=1-205&t=zq0mguDAKfVCwfC6-0&scaling=scale-down&content-scaling=fixed&page-id=0%3A1")
    qr.make(fit=True)
    # Crear la imagen del QR
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    return img


def create_image_center (img, logo):
    logo =Image.open(logo)
    # Calcular las dimensiones del logo
    basewidth = 100  # Puedes ajustar el tamaño del logo aquí
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)

    # Crear un recuadro blanco más grande que el logo
    logo_w, logo_h = logo.size
    white_box_size = (logo_w + 20, logo_h + 20)  # Ajusta el tamaño del recuadro blanco aquí
    white_box = Image.new('RGB', white_box_size, 'white')

    # Crear un borde negro alrededor del recuadro blanco
    black_border_size = (white_box_size[0] + 4, white_box_size[1] + 4)
    black_border = Image.new('RGB', black_border_size, 'black')

    # Calcular las posiciones
    center_pos = ((img.size[0] - black_border_size[0]) // 2, (img.size[1] - black_border_size[1]) // 2)
    white_box_pos = ((black_border_size[0] - white_box_size[0]) // 2, (black_border_size[1] - white_box_size[1]) // 2)
    logo_pos = ((white_box_size[0] - logo_w) // 2, (white_box_size[1] - logo_h) // 2)

    # Pegar el borde negro en el QR
    img.paste(black_border, center_pos)

    # Pegar el recuadro blanco en el borde negro
    white_box_pos = (center_pos[0] + white_box_pos[0], center_pos[1] + white_box_pos[1])
    img.paste(white_box, white_box_pos)

    # Pegar el logo en el recuadro blanco
    logo_pos = (white_box_pos[0] + logo_pos[0], white_box_pos[1] + logo_pos[1])
    img.paste(logo, logo_pos, mask=logo)

    # Guardar la imagen final
    img.save("logo_.png")
    return img

def QR_format(image_path):
    img = create_QR()
    img = create_image_center(img, image_path)