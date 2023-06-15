import os
import tensorflow as tf
import tensorflow_hub as hub

from pablo_app.style_transfer.utils import load_img, tensor_to_image

os.environ["TFHUB_MODEL_LOAD_FORMAT"] = "COMPRESSED"
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

hub_model_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
hub_model = hub.load(hub_model_url)

def transfer_style(content_path, style_path):
    content_image = load_img(content_path, 1024)
    style_image = load_img(style_path, 290)

    stylized_image = hub_model(tf.constant(content_image),
                               tf.constant(style_image))[0]
    return tensor_to_image(stylized_image)
