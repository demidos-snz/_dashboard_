import base64


def b64_image(image_filename: str) -> str:
    with open(file=image_filename, mode='rb') as f:
        image: bytes = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
