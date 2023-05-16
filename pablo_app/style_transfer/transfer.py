import os
import tensorflow as tf
import tensorflow_hub as hub

from pablo_app.style_transfer.utils import load_img, tensor_to_image

os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

hub_model_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"


def transfer_style(content_path, style_path):
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    hub_model = hub.load(hub_model_url)

    print(repr(hub_model))

    stylized_image = hub_model(tf.constant(content_image),
                               tf.constant(style_image))[0]
    return tensor_to_image(stylized_image)
