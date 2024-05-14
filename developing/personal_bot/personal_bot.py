import argparse
import itertools
import pathlib

import gradio as gr
import ollama
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to generate responses using the Llama3 model
def personal_context(image_path: pathlib.Path, person: str) -> str:
    logger.info("going to understand: '%s'", image_path)

    if image_path.is_dir():
        images_txts = itertools.chain.from_iterable(
            image_path.glob(pattern) for pattern in ['*.txt']
        )
    else:
        raise ValueError("image_path must be a directory")
    context = ""
    for image_txt in images_txts:
        logger.info("processing: '%s'", image_txt)
        image_txt = image_txt.with_suffix('.txt')
        with open(image_txt, 'rb') as image_file:
            context += "\n" + (image_file.read()).decode('utf-8')
    prompt = f"""
SYSTEM:
- You respond as a helpful assistant called "{person}" who is described by the context below.
- You can only respond with information from the context and nothing else.
- Reply as if you are Adrian and have the same interests as described in the context.
- If a question is asked that cannot be answered from the context, you respond with "I don't know".
- Answer in no more than 50 words.
CONTEXT:
{context}
"""
    logger.info(f"Using this prompt:\n{prompt}")
    return prompt


def generate_response(host: str, image_dir: str, person: str):
    context = personal_context(pathlib.Path(image_dir), person)
    client = ollama.Client(host=f"{host}:11434")
    logger.info("Pulling model: llama3:8b")
    client.pull("llama3:8b")
    logger.info("Pulled model: llama3:8b")

    def inner(question: str) -> str:
        prompt = context + f"""
Question: {question}
"""
        logger.info(f"Using this prompt:\n{prompt}")

        response = client.chat(model='llama3:8b', messages=[{
            'role': 'user',
            'content': prompt,
        }], options={

        })
        return response['message']['content']

    return inner


# Gradio interface


def main():
    parser = argparse.ArgumentParser(description='Process image and return API response.')
    parser.add_argument('image_path', help='The path to the image file')
    parser.add_argument('--host', default='host.docker.internal', help='Server host')
    parser.add_argument('--person', required=True, help='Who are you')
    args = parser.parse_args()
    iface = gr.Interface(
        fn=generate_response(args.host, args.image_path, args.person),
        inputs="text",
        outputs="text",
        title=f"I am {args.person}, ask me about my interests",
        description="Come on give it a try!"
    )

    # Launch the app
    iface.launch(server_name="0.0.0.0")


if __name__ == "__main__":
    main()
