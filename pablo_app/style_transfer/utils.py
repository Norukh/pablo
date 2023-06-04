import tensorflow as tf
import PIL.Image
import numpy as np


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


def original_image_path(style_image_path: str) -> str:
    if style_image_path is not None:
        split_image_path = style_image_path.split("/")
        image_name = "_".join(split_image_path[-1].split("_")[:-1])
        return "/".join(split_image_path[:3] + ["original"] + [image_name] + split_image_path[4:])

    return ""


def load_img(path_to_img, max_dim=512):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img
