from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoProcessor, AutoModelForZeroShotImageClassification
import base64
from io import BytesIO
from PIL import Image
from model import generateimage

#Allowing every front-end application 
origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

class ImageData(BaseModel):
    image: str

@app.get("/image-from-text/{promt}")
async def root(promt):
    print(promt)
    generateimage(promt)
    return FileResponse(f"gen-image.jpg")

@app.post("/image2text")
def image2text(body: ImageData):
    base64_string = body.image 
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))

    processor = AutoProcessor.from_pretrained("openai/clip-vit-large-patch14") 

    model = AutoModelForZeroShotImageClassification.from_pretrained("openai/clip-vit-large-patch14")



    features = ["Jacket", "T-Shirt", "Shoe", "Pants", "Hats", "Glasses", "Dress"]

    colors = ["Black", "Red", "Blue", "Yellow", "Green", "White", "Brown", "Gray"]

    inputs = processor(
        text=features,
        images=image,
        return_tensors="pt",
        padding=True,
    )

    color_inputs = processor(
        text=colors,
        images=image,
        return_tensors="pt",
        padding=True,
    )

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    color_outputs = model(**color_inputs)
    color_logits_per_image = color_outputs.logits_per_image
    color_probs = color_logits_per_image.softmax(dim=1)

    prob_list = probs.detach().numpy().tolist()

    color_prob_list = color_probs.detach().numpy().tolist()

    output = dict(zip(features, prob_list[0]))

    print(output)

    clothing_item = max(output, key=output.get)

    color_output = dict(zip(colors, color_prob_list[0]))

    print(color_output)

    color = max(color_output, key=color_output.get)

    return color + " " + clothing_item


