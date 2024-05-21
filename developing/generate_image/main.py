import requests
import argparse
import base64
from PIL import Image
from io import BytesIO
import json


def generate_images(host, description, style, output_filename):
    url = f"http://{host}:8080/generate/"  # Construct the URL based on the host
    raise Exception("Needs to be implemented.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using a Stable Diffusion API.")
    parser.add_argument("-H", "--host", default="server", help="The host address of the API (e.g., localhost:8000)")
    parser.add_argument("-d", "--description", required=True, help="The description of the image to generate")
    parser.add_argument("-s", "--style", required=True, help="The style of the image")
    parser.add_argument("-o", "--output_filename", required=True,
                        help="The base filename for the output images (e.g., lion_image)")

    args = parser.parse_args()

    generate_images(args.host, args.description, args.style, args.output_filename)
