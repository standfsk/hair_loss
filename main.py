from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import base64
import os
from pathlib import Path
from PIL import Image

from model import CNN
import torch
import torchvision.transforms as transforms
from torchvision.transforms import Compose, Normalize

# 업로드된 이미지를 저장할 디렉토리
upload_dir = "uploads"

# 업로드 폴더 생성
Path(upload_dir).mkdir(parents=True, exist_ok=True)

# FastAPI 설정
app = FastAPI()
app.mount('/static', StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

# 모델 load
model = CNN()
model.load_state_dict(torch.load("CNN100.pt"))
model.eval()

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

# 추론
@app.post("/inference/")
async def inference():
    # 업로드된 이미지가 있는지 확인
    if os.path.exists(f"{upload_dir}/uploaded_image.jpg"):
        with open(f"{upload_dir}/uploaded_image.jpg", "rb") as image_file:
            # 이미지 로드
            img = Image.open(image_file)
            
            # 데이터 전처리
            transform = Compose([
                transforms.ToTensor(),
                transforms.Resize((224, 224)),
                Normalize(mean=(0.4914, 0.4822, 0.4465), std=(0.247, 0.243, 0.261))
            ])
            img = transform(img).unsqueeze(0)

            # 모델을 사용하여 추론 수행
            with torch.no_grad():
                result = model(img)

            # 결과 후처리
            if result.item() > 0.9:
                predt = '탈모'
            else:
                predt = '탈모 X'

            # 결과를 응답으로 반환
            return JSONResponse(content={"predt": predt, "predn": round(result.item(), 6)})
    else:
        return JSONResponse(content={"error": "업로드된 이미지를 찾을 수 없음"})
    