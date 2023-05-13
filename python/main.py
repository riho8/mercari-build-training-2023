import os
import logging
import pathlib
import json
import hashlib
import sqlite3
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

# curl -X POST --url 'http://localhost:9000/items' -F 'name=jacket' -F 'category=fashion' -F 'image=@images/local_image.jpg'
@app.post("/items")
def add_item(name: str = Form(...),category: str = Form(...),image:UploadFile = File(...) ):
    image = images / image.filename
    with open(image, "rb") as f:
        image_hash = hashlib.sha256(f.read()).hexdigest()
    image_name = str(image_hash) + ".jpg"

    #データベースに接続
    conn = sqlite3.connect('../db/mercari.sqlite3', check_same_thread=False)
    #カーソルを取得
    c = conn.cursor()
    #データを追加
    c.execute("INSERT INTO items (name, category, image_name) VALUES (?, ?, ?)", (name, category, image_name))
    #変更を反映するために必要
    conn.commit()
    #データベースとの接続を切る
    conn.close()
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

#curl -X GET 'http://127.0.0.1:9000/items'
@app.get("/items")
def get_items():
    #データベースに接続
    conn = sqlite3.connect('../db/mercari.sqlite3', check_same_thread=False)
    #カーソルを取得
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    #データを一括で取り出す
    data = c.fetchall()
    conn.close()
    return data

#curl -X GET 'http://127.0.0.1:9000/items/1'
@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    id = item_id
    with open('items.json', 'r') as f:
        data = json.load(f)
    return data["items"][id -1]

#curl -X GET 'http://127.0.0.1:9000/search?keyword=jacket'
@app.get("/search")
def search_item(keyword: str):
    conn = sqlite3.connect('../db/mercari.sqlite3', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM items WHERE name LIKE ?", ('%' + keyword + '%',))
    data = c.fetchall()
    conn.close()
    return data

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
