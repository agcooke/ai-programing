import asyncio
import base64
import logging
from io import BytesIO

import torch
from diffusers import AutoPipelineForText2Image, StableDiffusionXLPipeline
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageRequest(BaseModel):
    description: str
    style: str


app = FastAPI()


async def initialize_pipeline():
    logger.info("Downloading Stable Diffusion model...")
    localPipe = StableDiffusionXLPipeline.from_pretrained("stabilityai/sdxl-turbo")

    device = "cpu"
    if torch.cuda.is_available():
        logger.info("CUDA available. Using CUDA for Stable Diffusion.")
        device = "cuda"
    elif torch.backends.mps.is_available():
        logger.info("MPS available. Using MPS for Stable Diffusion.")
        localPipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")
        device = "mps"

    localPipe = localPipe.to(device)
    localPipe.enable_attention_slicing()
    logger.info(f"Stable Diffusion model initialized to device: {device}")
    return localPipe


@app.on_event("startup")
async def startup_event():
    logger.info("startup event called")
    global pipe
    pipe = await initialize_pipeline()
    logger.info("startup event finished")


@app.post("/generate/")
async def generate(request: ImageRequest):
    prompt = f"DESCRIPTION: {request.description}\nSTYLE: {request.style}"
    logger.info(f"Processing: '{prompt}'")
    images = pipe(prompt=prompt, height=1024, width=1024, num_inference_steps=6, guidance_scale=0.0,
                  num_images_per_prompt=2,
                  negative_prompt="extra limbs, extra heads, extra legs, (mutated hands and fingers:1.5), (long neck:1.3), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra digit, fewer digits, cropped, worst quality, low quality"
                  ).images
    logger.info(f"images length: {len(images)}")
    images = images[:2]

    base64_images = []
    for image in images:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_images.append(base64.b64encode(buffered.getvalue()).decode())

    await asyncio.sleep(0.1)  # Small delay to allow other tasks to run
    return {"images": base64_images}


@app.get("/")
async def root():
    return {"message": "Hello World"}
