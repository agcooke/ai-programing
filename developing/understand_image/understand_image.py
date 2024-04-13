import argparse
import base64
import itertools
import json
import logging
import pathlib
from typing import NoReturn

import requests
from developing.ollama_api.print_output import parse_output

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def understand_image(image_path: pathlib.Path, host: str) -> NoReturn:
    logger.info("going to understand: '%s'", image_path)

    if image_path.is_dir():
        images = itertools.chain.from_iterable(
            image_path.glob(pattern) for pattern in ['*.JPEG', '*.png', '*.jpg', '*.JPG', '*.jpeg', '*.PNG']
        )
    else:
        images = [image_path]

    for image in images:
        logger.info("processing: '%s'", image)
        image_txt = image.with_suffix('.txt')
        if image_txt.exists():
            logger.info("skipping existing file: '%s'", image_txt)
            continue
        with open(image, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {'Content-type': 'application/json'}
        data = json.dumps({
            "model": "llava",
            "prompt": "What is in this picture?",
            "stream": True,
            "images": [encoded_string]
        })

        response = requests.post(f'http://{host}:11434/api/generate', headers=headers, data=data)
        logger.info("Finished understanding:")

        description = parse_output(response, "response")
        with open(image_txt, "w") as image_desc:
            image_desc.write(description)


def main():
    parser = argparse.ArgumentParser(description='Process image and return API response.')
    parser.add_argument('image_path', help='The path to the image file')
    parser.add_argument('--host', default='ollama', help='Server host')
    args = parser.parse_args()
    understand_image(pathlib.Path(args.image_path), args.host)


if __name__ == "__main__":
    main()
