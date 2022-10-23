import base64
import io

import numpy as np
import requests
from PIL import Image
from loguru import logger


class ImageHandler:
    supported_image_types = [
        "image/png", "image/jpg", "image/jpeg", "image/webp"
    ]

    @staticmethod
    def base64_to_pillow_image(base64_image: str) -> Image:
        logger.info("Processing")
        b64image_type = base64_image.split(":")[1].split(";")[0]
        logger.info(b64image_type)
        image_data = base64_image.split(":")[1].split(";")[-1].split(",")[1]
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))

        return img

    @staticmethod
    def formfile_to_pillow_image(bytes_image) -> Image:
        logger.info("Processing")
        image = Image.open(io.BytesIO(bytes_image))
        logger.info("Done")
        return image

    @staticmethod
    def url_to_pillow_image(url_image: str) -> Image:
        logger.info("Processing")
        res = requests.get(url_image, allow_redirects=True)

        if res.status_code == 200:
            logger.info("Fround Image will start download")
            image_format = res.headers["content-type"]
            logger.info(image_format)

            if image_format in ImageHandler.supported_image_types:

                image = Image.fromarray(np.frombuffer(res.content, np.uint8))
                logger.info("Done")
                return image

            else:
                logger.error("Image Not Support")
                return None
        else:
            logger.error("Image Not Fround")
            return None
