from PIL import Image


def prepare_image(uploaded_file):
    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    return image
