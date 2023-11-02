# 탈모 분류 프로젝트
![image](https://github.com/cshyo1004/hair_loss/assets/60250322/a784f286-2e81-4e42-a6dc-c5c35aada2bf)

## 프로젝트 개요
집에서 간편하게 탈모인지 아닌지 알아보기 위한 솔루션
- 탈모 검사 병원 찾기 힘듬
- 예약 잡기 힘듬
- 비용 발생

## 목표
이미지를 통해 탈모인지 아닌지 판별하는 솔루션 구축

## Data
- <a href="https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=data&dataSetSn=85">AIHUB 한국인 헤어스타일 이미지</a>
- 크롤링

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
  <br><img src="https://github.com/cshyo1004/hair_loss/assets/60250322/b58a2065-9ba2-417d-b059-5b0f18bc70be" width=500>

- VGG(pre-trained)
  <br><img src="https://github.com/cshyo1004/hair_loss/assets/60250322/d322b79a-0f01-4ce9-b1f4-8598020d1f85" width=500>

- ResNet(pre-trained)
  <br><img src="https://github.com/cshyo1004/hair_loss/assets/60250322/66cb38da-c923-48ac-854d-4aa4ed36d1d6" width=500>

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
* train2 epoch32부터 error 발생으로 인해 loss와 accuracy값 이상
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
* train2 epoch32부터 error 발생으로 인해 loss와 accuracy값 이상
|  | train1 | train2 |
| --- | --- | --- |
| test loss | 0.06 | 18.89 |
| test accuracy | 99.71 | 81.38 |

