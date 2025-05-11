from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32  # Change float16 to float32
)
pipe.to("cpu")

prompt = "iron man in party"
image = pipe(prompt, num_inference_steps=10).images[0] 

image.save("generated_image.png")

