import os
import logging
import pathlib
import json
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
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

#curl -X POST --url 'http://localhost:9000/items' -d 'name=jacket' -d 'category=fashion'
@app.post("/items")
def add_item(name: str = Form(...),category: str = Form(...)):
    item = {"name": name, "category": category}

    #import json 必要
    #items.jsonを開く
    f = open('items.json', 'r')
    #開いたファイルをjsonとして読み込む
    data = json.load(f)
    #読み込んだjsonにitemを追加
    data["items"].append(item)
    #書き込むファイルを開く
    f = open('items.json', 'w')
    #jsonを書き込む(辞書型のデータ)    
    json.dump(data, f)

    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

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