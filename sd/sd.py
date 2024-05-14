from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo")
pipe.to("mps")

prompt = "Show a picture with the text 'This is life', floating above a lake in the mountains. Only the text should appear, and only once."

image = pipe(prompt=prompt, height=1024, width=1024, num_inference_steps=6, guidance_scale=0.0).images[0]

image.save("my_stable_diffusion_image-surfer.png", "PNG")  # Replace with your desired filename
