updated_api_code = '''
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io
import random
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading AI model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
print("Model ready!")

def generate_accurate_caption(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    inputs = processor(image, return_tensors="pt")
    
    out = model.generate(
        **inputs,
        num_beams=5,
        temperature=0.7,
        max_new_tokens=40,
        repetition_penalty=1.2
    )
    
    return processor.decode(out[0], skip_special_tokens=True)

def style_caption(caption, style):
    if style == "poetic":
        return f"✨ {caption.lower()} ✨"
    
    elif style == "cinematic":
        return f"🎬 {caption.upper()} 🎬"
    
    elif style == "funny":
        funny_options = [
            f"Plot twist: {caption} 😂",
            f"POV: {caption} 🤣",
            f"Nobody:\nMe: {caption} 😎"
        ]
        return random.choice(funny_options)
    
    else:
        styles = [f"🌸 {caption} 🌸", f"✨ {caption} ✨", f"💫 {caption} 💫", f"📸 {caption} 📸"]
        return random.choice(styles)

def generate_captions(image, num_captions=3, style="creative"):
    if image is None:
        return ["Please upload an image"]
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    captions = []
    
    temps = [0.7, 0.8, 0.9, 0.85, 0.75]
    beams = [5, 4, 6, 3, 5]
    
    num = min(num_captions, 5)
    
    for i in range(num):
        inputs = processor(image, return_tensors="pt")
        
        out = model.generate(
            **inputs,
            num_beams=beams[i % len(beams)],
            temperature=temps[i % len(temps)],
            max_new_tokens=40,
            do_sample=True,
            repetition_penalty=1.2
        )
        
        base_caption = processor.decode(out[0], skip_special_tokens=True)
        styled = style_caption(base_caption, style)
        captions.append(styled)
    
    return captions

@app.get("/")
def root():
    return {"name": "AI Caption Generator", "version": "3.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/caption")
async def caption_image(
    file: UploadFile = File(...),
    num_captions: int = Form(3),
    style: str = Form("creative")
):
    if num_captions < 1 or num_captions > 5:
        num_captions = 3
    
    valid_styles = ["creative", "poetic", "cinematic", "funny"]
    if style not in valid_styles:
        style = "creative"
    
    try:
        image = Image.open(io.BytesIO(await file.read()))
        captions = generate_captions(image, num_captions, style)
        
        return {
            "success": True,
            "num_captions": len(captions),
            "style": style,
            "captions": captions
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
'''

with open("api.py", "w", encoding="utf-8") as f:
    f.write(updated_api_code)

print("api.py UPDATED with better captions and real emojis!")