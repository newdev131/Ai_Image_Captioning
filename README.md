# AI Image Caption API

## Live API
https://arfanaeem-image-caption-api.hf.space

## API Endpoints

| Endpoint | Method | What it does |
|----------|--------|--------------|
| / | GET | API info |
| /health | GET | Check if working |
| /caption | POST | Upload image, get captions |

## How to Use

### Test API
GET https://arfanaeem-image-caption-api.hf.space/health

### Generate Captions
POST https://arfanaeem-image-caption-api.hf.space/caption


**Parameters:**
- file: Your image (required)
- num_captions: 1-5 (default: 3)
- style: creative, poetic, cinematic, funny (default: creative)

## Response Example
```json
{
  "success": true,
  "captions": ["✨ a dog running ✨", "🌸 playful puppy 🌸"]
}

import requests

url = "https://arfanaeem-image-caption-api.hf.space/caption"
files = {"file": open("image.jpg", "rb")}
data = {"num_captions": 3, "style": "creative"}

response = requests.post(url, files=files, data=data)
print(response.json())

```

##Technologies
.FastAPI
.BLIP Model (Hugging Face)
.Docker

##Author
Arfa Naeem | Machine Learning Project | March 2026
