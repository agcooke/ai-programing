import argparse
import json
import logging
from typing import NoReturn

import requests
import developing.ollama_api.print_output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_llava_model(host: str, tag: str) -> NoReturn:
    url = f'http://{host}:11434/api/create'
    headers = {'Content-Type': 'application/json'}
    data = {
        "name": "llava",
        "modelfile": f"FROM llava:{tag}\nSYSTEM You understand images."
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        logger.info("Llava model creation succeeded:")
        developing.ollama_api.print_output.parse_output(response)
    else:
        logger.info("Llava model creation failed: {}:{}", response.status_code, response.text)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pull the llava image understanding library.')
    parser.add_argument('--host', default='ollama', help='Server host')
    parser.add_argument('--tag', default='latest', help='Use different tags of the llava model.')
    args = parser.parse_args()
    create_llava_model(args.host, args.tag)
