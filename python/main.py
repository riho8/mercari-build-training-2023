import os
import logging
import pathlib
import json
import hashlib
from fastapi import FastAPI, Form, HTTPException ,UploadFile,File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

#uvicorn main:app --reload --port 9000
app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.DEBUG
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, world!"}

# curl -X POST \
#   --url 'http://localhost:9000/items' \
#   -F 'name=jacket' \
#   -F 'category=fashion' \
#   -F 'image=@images/local_image.jpg'
@app.post("/items")
def add_item(name: str = Form(...),category: str = Form(...),image:UploadFile = File(...) ):
    # image.filename: local_image.jpg
    image = images / image.filename
    #バイナリで開く
    f = open(image, "rb")
    # ハッシュ値を取得
    image_hash = hashlib.sha256(f.read()).hexdigest()
    image_filename = str(image_hash) + ".jpg"
    item = {"name": name, "category": category, "image_filename": image_filename}

    f = open('items.json', 'r')
    data = json.load(f)
    data["items"].append(item)
    f = open('items.json', 'w')
    json.dump(data, f)

    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

#curl -X GET 'http://127.0.0.1:9000/items'
@app.get("/items")
def get_items():
    f = open('items.json', 'r')
    data = json.load(f)
    return data

#curl -X GET 'http://127.0.0.1:9000/items/1'
@app.get("/items/{item_id}")
def get_item_by_id(item_id):
    id = int(item_id)
    f = open('items.json', 'r')
    data = json.load(f)
    return data["items"][id -1]

@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)