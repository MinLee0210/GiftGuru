import requests
from PIL import Image

import yaml

def yaml_read(dir): 
    with open(dir) as f:
        my_dict = yaml.safe_load(f)
    return my_dict

def load_image(image_str: str) -> Image.Image:
    if image_str.startswith("http"):
        image = Image.open(requests.get(image_str, stream=True).raw).convert("RGB")
    else:
        image = Image.open(image_str).convert("RGB")

    return image