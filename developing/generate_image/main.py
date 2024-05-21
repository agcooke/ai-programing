import requests
import argparse
import base64
from PIL import Image
from io import BytesIO
import json


def generate_images(host, description, style, output_filename):
    url = f"http://{host}:8080/generate/"  # Construct the URL based on the host

    # Prepare the request data
    data = {"description": description, "style": style}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        result = response.json()
        images = result.get("images", [])

        if not images:
            raise Exception("No images were generated.")

        # Process and save the images
        for i, image_data in enumerate(images[:2]):  # Limit to 2 images
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            filename = f"{output_filename}-{i + 1}.png"
            image.save(filename)
            print(f"Image saved as {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except Exception as e:
        print(f"Error processing images: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using a Stable Diffusion API.")
    parser.add_argument("-H", "--host", default="server", help="The host address of the API (e.g., localhost:8000)")
    parser.add_argument("-d", "--description", required=True, help="The description of the image to generate")
    parser.add_argument("-s", "--style", required=True, help="The style of the image")
    parser.add_argument("-o", "--output_filename", required=True,
                        help="The base filename for the output images (e.g., lion_image)")

    args = parser.parse_args()

    generate_images(args.host, args.description, args.style, args.output_filename)
