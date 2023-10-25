from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import base64
import os
from pathlib import Path

# 업로드된 이미지를 저장할 디렉토리
upload_dir = "uploads"

# 업로드 폴더 생성
Path(upload_dir).mkdir(parents=True, exist_ok=True)

# FastAPI 설정
app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# main
@app.get("/", response_class=HTMLResponse)
async def main():
    with open("templates/index.html", encoding='utf-8') as f:
        content = f.read()

    # 이미지를 읽어서 Base64로 변환
    image_base64 = ""
    if os.path.exists(f"{upload_dir}/uploaded_image.jpg"):
        with open(f"{upload_dir}/uploaded_image.jpg", "rb") as image:
            image_base64 = base64.b64encode(image.read()).decode()

    # HTML 템플릿에 이미지 URL 삽입
    content = content.replace("{{image}}", image_base64)
    
    return HTMLResponse(content)

# 업로드
@app.post("/upload/")
async def upload_image(file: UploadFile):
    # 이미지를 업로드 디렉토리에 저장
    with open(f"{upload_dir}/uploaded_image.jpg", "wb") as image:
        shutil.copyfileobj(file.file, image)

    # 업로드 후 JSON 응답을 반환
    return JSONResponse({"filename": "uploaded_image.jpg"})

# 리셋
@app.post("/reset/")
async def reset_image():
    # 이미지를 초기화 (삭제)
    if os.path.exists(f"{upload_dir}/uploaded_image.jpg"):
        os.remove(f"{upload_dir}/uploaded_image.jpg")

    # 초기화 후 JSON 응답을 반환
    return JSONResponse(content={"success": True})

# # 이미지 갱신
# @app.get("/get_image/", response_class=JSONResponse)
# async def get_image():
#     # 이미지를 읽어서 Base64로 변환
#     image_base64 = ""
#     if os.path.exists(f"{upload_dir}/uploaded_image.jpg"):
#         with open(f"{upload_dir}/uploaded_image.jpg", "rb") as image:
#             image_base64 = base64.b64encode(image.read()).decode()
    
#     return {"image": image_base64}
