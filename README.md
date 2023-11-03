# 탈모 분류 프로젝트
<img src="https://github.com/cshyo1004/hair_loss/assets/60250322/dd00720e-f756-4f14-898f-7ba2187d38db" width=800>

## 프로젝트 개요
집에서 간편하게 탈모인지 아닌지 알아보기 위한 솔루션
- 탈모 검사 병원 찾기 힘듬
- 예약 잡기 힘듬
- 비용 발생

## 목표
이미지를 통해 탈모인지 아닌지 판별하는 솔루션 구축

## Data
### AIHUB 한국인 헤어스타일 이미지
- https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=85
- 다양한 한국인 이미지 데이터로부터 헤어스타일 인식 및 헤어스타일만을 합성하는 한국인 헤어스타일 이미지 AI 데이터셋
- 사용 클래스: [가르마, 기타남자스타일, 남자일반숏, 댄디, 리젠트, 소프트블록댄디, 쉐도우, 쉼표, 스핀스왈로, 시스루댄디, 애즈, 원블럭댄디, 포마드]
- mqset 데이터 중 특정 조건에 해당하는 이미지 파일을 추출하고 해당 이미지 중 2,000개 랜덤 선택하여 비탈모 데이터로 활용
  - horizontal: 140 - 170 // 뒤통수가 보이는 각도를 확인하여 해당 각도에 해당하는 데이터 사용
  - vertical: '상' // 최대한 정수리가 보이는 각도를 사용하기 위해서 위쪽에서 아래로 찍힌 데이터 사용
  - gender: '남' // 크롤링 데이터 대다수가 남자 데이터이기 때문에 성별을 따로 지정하여 데이터 사용
  - color: '블랙' // 크롤링 데이터 대다수가 검은색 머리카락 데이터이기 때문에 머리색을 따로 지정하여 데이터 사용
### 크롤링
- 구글 이미지 검색을 통해 탈모 데이터 크롤링
### 데이터 전처리
- 이미지 크기는 (512 x 512)로 조정 / 학습 시 (224 x 224)
- 이미지 확장자는 .jpg로 변환
- 기준에 부합하지 않는 데이터 제거
  
|정수리가 보이지 않는 경우|두상이 보이지 않는 경우|이미지에 글자가 포함되어 있는 경우|애니매이션 사진인 경우|머리에 손이 닿아있는 경우|
|---|---|---|---|---|
|<img src="https://github.com/cshyo1004/hair_loss/assets/60250322/938822b4-d1ee-4313-8df8-b9cf782406fd" width=200 height=200>|<img src="https://github.com/cshyo1004/hair_loss/assets/60250322/ba9d4ba1-73eb-4988-b6a6-13b9edd02892" width=200 height=200>|<img src="https://github.com/cshyo1004/hair_loss/assets/60250322/cd105c7c-e45e-40ca-859e-d0ef3570a273" width=200 height=200>|<img src="https://github.com/cshyo1004/hair_loss/assets/60250322/89c7bfa7-ad5e-4847-8019-764f8f52cc8a" width=200 height=200>|<img src="https://github.com/cshyo1004/hair_loss/assets/60250322/afb195ff-615a-4346-9c9f-ffaae8284f1c" width=200 height=200>|

### 데이터 증강
- 탈모 데이터
  - cutout
  - blur
  - 데이터 수: 2,789 → 8,367
- 비탈모 데이터
  - cutout
  - blur
  - noise
  - cutout + blur
  - cutout + noise
  - blur + noise
  - cutout + blur + noise
  - 데이터 수: 239 → 1,912

## 학습 환경
- 로컬
  - CPU: 인텔 i7-9700
  - Memory: DDR4 16G(Dual)
  - GPU: GTX 1650 4G
  - torch 2.0.0+cuda11.8
- 외부
  - Google Colab
- 세부 설정
  - data split: 8:1:1
  - epoch: 100
  - batch_size: [16,32]
  - learning_rate: [0.0001, 0.001]
  - optimizer: Adam
  - earlystopping: patience=5, min_delta=0.005

## Model
- CNN(self-implemented)
  <br><img src="https://github.com/cshyo1004/hair_loss/assets/60250322/a9040304-ddd0-49c7-b2f5-712282255b10" width=500>

- VGG(pre-trained)
  <br><img src="https://github.com/cshyo1004/hair_loss/assets/60250322/2ed770eb-d137-4235-a297-fb32f8012fbe" width=500>

- ResNet(pre-trained)
  <br><img src="https://github.com/cshyo1004/hair_loss/assets/60250322/d00ab2f4-ef26-4135-b988-d8c0c21aebd8" width=500>

## Performance
### CNN
|  | train1 | train2 | train3 | train4 |
| --- | --- | --- | --- | --- |
| batch_size | 32 | 16 | 32 | 16 |
| learning_rate | 0.0001 | 0.0001 | 0.001 | 0.001 |
| 학습 시간 | 1.8h | 1.9h | 1.9h | 1.8h |
| train loss | 5.07E-06 | 1.042E-07 | 5.891E-20 | 1.711E-05 |
| train accuracy | 99.98 | 99.97 | 99.97 | 99.97 |
| val loss | 0.009 | 0.006 | 0.017 | 0.003 |
| val accuracy | 99.82 | 99.82 | 99.64 | 99.94 |

### VGG
|  | train1 | train2 |
| --- | --- | --- |
| batch_size | 32 | 16 |
| learning_rate | 0.0001 | 0.0001 |
| 학습 시간 | 3.4h | 3.8h |
| train loss | 2.3E-08 | 2.2E-29 |
| train accuracy | 99.95 | 99.92 |
| val loss | 0.07 | 0.081 |
| val accuracy | 99.82 | 99.7 |

### ResNet
|  | train1 | train2 |
| --- | --- | --- |
| batch_size | 32 | 16 |
| learning_rate | 0.0001 | 0.0001 |
| 학습 시간 | 7.9h | 7.9h |
| train loss | 0.3937 | 0.3980 |
| train accuracy | 82.69 | 82.92 |

## Evaluation
### CNN
|  | train1 | train2 | train3 | train4 |
| --- | --- | --- | --- | --- |
| test loss | 0.0101 | 0.006 | 0.019 | 0.006 |
| test accuracy | 99.708 | 99.81 | 99.61 | 99.76 |

### VGG
|  | train1 | train2 |
| --- | --- | --- |
| test loss | 0.06 | 18.89 |
| test accuracy | 99.71 | 81.38 |

