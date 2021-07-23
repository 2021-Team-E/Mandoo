한국어 | [English](README_en.md)

---

# **QUIZRIX(허락 필요)**

- 학습지 이미지 데이터에서 문항정보를 추출해 데이터베이스에 저장 후 해당 내용을 사용자의 브라우저에서 접속 가능하도록하는 플랫폼

1. 학습 문제의 이미지를 업로드 방식으로 등록한다.
<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126748956-5bf7503e-575a-4008-83e1-9632de129c2c.png">
 </p>
2. 학습지 이미지 데이터에서 딥러닝을 이용하여 문항정보를 추출한다.
<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126749134-2e804fb4-e62b-4e68-a1aa-4cdc033409c3.png">
</p>

<br>

     최종본 gif 추가

> 본 프로젝트는 코드넛 'QUIZRIX' 사업의 일부 프로토타입 제작을 위해 진행되었습니다.

## **System Architecture ->검사 받고 최종 올려둘게요**

<p align="center">  
  <img src="https://user-images.githubusercontent.com/52441923/126756283-16c5dd0b-8f84-4aab-81f1-b7e4ea4cc171.jpg">
</p>

## **Description**

웹페이지에 문제 이미지를 첨부하면 문항 / 보기 / 선지로 세분화하여 데이터베이스에 저장합니다.

> 현재 개발 중에 있습니다.

<br>

## **Tech Stack**

<br>

| 분류          | 기술                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 개발환경      | ![NHN](https://img.shields.io/badge/NHN_Cloud_Ubuntu-20.04-blue?logo=ubuntu) ![S3](https://img.shields.io/badge/S3-green?logo=AmazonS3) ![Docker](https://img.shields.io/badge/docker-blue?logo=docker)                                                                                                                                                                                                                                                                                                                                                                                                    |
| Front-end     | ![react](https://img.shields.io/badge/react-9cf?logo=react) ![Javascript](https://img.shields.io/badge/javascript-ES6+-yellow?logo=javascript) ![Bootstrap](https://img.shields.io/badge/bootstrap-9cf?logo=bootstrap) ![axios](https://img.shields.io/badge/axios-9cf?color=purple) ![Styled-components](https://img.shields.io/badge/styled_components-DB7093?logo=styled-components)                                                                                                                                                                                                                    |
| Back-end      | ![Flask](https://img.shields.io/badge/flask-1.1.2-green?logo=flask) ![Python](https://img.shields.io/badge/python-3.7.6-skyblue?logo=python) ![Gunicorn](https://img.shields.io/badge/gunicorn-darkgreen?logo=gunicorn) ![Postman](https://img.shields.io/badge/postman-pink?logo=postman) ![Swagger](https://img.shields.io/badge/swagger-darkgreen?logo=swagger)                                                                                                                                                                                                                                         |
| DB            | ![MongoDB](https://img.shields.io/badge/mongodb-blue?logo=mongodb)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Deep learning | ![Pytorch](https://img.shields.io/badge/pytorch-blue?logo=pytorch) ![Colab](https://img.shields.io/badge/colab-darkgreen?logo=GoogleColab)                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Etc           | ![Nginx](https://img.shields.io/badge/Nginx-brightgreen?logo=nginx) ![github](https://img.shields.io/badge/github-gray?logo=github) ![VScode](https://img.shields.io/badge/VScode-blue?logo=visual-studio-code) ![Google Cloud Platform](https://img.shields.io/badge/Google_Cloud_Platform-VM_instance-red?logo=gcp) ![AWS](https://img.shields.io/badge/AWS-EC2_instance-orange?logo=aws) ![Prometheus](https://img.shields.io/badge/Prometheus-green?logo=Prometheus) ![Grafana](https://img.shields.io/badge/Grafana-green?logo=Grafana) ![Redis](https://img.shields.io/badge/Redis-green?logo=redis) |

## **PORTS**

| Name             | Port       | Description                                                                                                                                   |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Nginx            | 80         | 가벼움과 높은 성능을 목표로 하는 웹서버로 서버로서의 역할과 프록시로서의 역할을 수행합니다.                                                   |
| React(on Nginx)  | 80, 3000   | 학습 문제의 이미지를 업로드 방식으로 등록하면, 해당 문제의 문항내용, 보기, 선지를 분류하여 텍스트 및 이미지로 저장할 수 있는 UI를 제공합니다. |
| Flask + Gunicorn | 8000, 5000 | QUIZRIX의 서버. 모든 행동의 중심에 위치하여 웹서버, Cloud Storage, DB 간의 소통을 담당합니다.                                                 |
| Mongo DB         | 27017      | Database                                                                                                                                      |
| Grafana          | 3001       | cAdvisor, Prometheus, NodeExporter를 통해 전달받은 시간별 매트릭 데이터를 시각화하여 대시보드로 제공해줍니다.                                 |
| cAdvisor         | 8080       | 사용중인 도커 컨테이너의 리소스 사용량을 측정하여 시계열 매트릭 데이터화합니다.                                                               |
| Prometheus       | 9090       | cAdvisor, node exporter의 시계열 매트릭 데이터를 수집하여 시스템 모니터링 및 경고합니다.                                                      |
| Node Exporter    | 9100       | 서버의 cpu, 메모리, 디스크, 네트워크 사용량등 호스트 관련 매트릭 데이터를 수집하여 api로 노출시킵니다.                                        |

<br>

## **AI**

### flow

<img width="476" alt="AI Flow" src="https://user-images.githubusercontent.com/80239146/126749561-c724903b-9bf2-4975-968b-6a6f1fe41a71.png">

<br>

### 결과

- Model 1
  <img width="532" alt="model1" src="https://user-images.githubusercontent.com/80239146/126751834-81adeca3-36f7-48c4-9ea4-e360042f7551.PNG">

- Model 2  
  <img width="571" alt="model2" src="https://user-images.githubusercontent.com/80239146/126751880-3cc7c43f-ee20-4f38-a72e-87b80769dfa7.PNG">

## **Frontend: React**

#### file tree install

<br>

## **Backend: Flask**

#### file tree install

<br>

## **Installation**

> ### Deploy

### **Github**

- Clone Repository

  ```bash
  git clone https://github.com/2021-Team-E/Mandoo.git
  ```

<br>

### **Front-end** setting

- package.json

  ```json
  {
    ...

    "proxy": "http://<ip>:<server_port>",

    ...
  }
  ```

- config.js

  ```javascript
  export const USER_SERVER = "http://<ip>:<server_port>";
  ```

<br>

### **Back-end** Setting

- app.py

  ```python
  mongo = MongoClient('mongo_db', 27017)
  ```

- detection.py

  ```python
  #서버 환경에서의 tesseract.exe 경로로 설정
  pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"
  ```

- requirements.txt  
  Dockerfile에서 따로 설치하는 라이브러리를 주석처리합니다.

  ```
  # requirements.txt

  ...

  # tesseract-ocr
  # pytesseract

  …
  ```

- s3.py <— Make new file name 's3.py' in ./Backend

  ```python
  AWS_ACCESS_KEY = <AWS ACCESS KEY>
  AWS_SECRET_KEY = <AWS SECRET KEY>
  BUCKET_NAME = <AWS S3 bucket name>
  ```

### **Docker** 🐳

```bash
docker-compose up —build
```

### Docker

### 배포

## API

## gif 이미지 넣는거/ 수정하는거

## 멤버 소개

<br>

## **Members**

|     이름 | 개발분야                           | 담당                                  | 소개페이지                                         |
| -------: | ---------------------------------- | ------------------------------------- | -------------------------------------------------- |
|   최윤재 | Front-end, Back-end, Deep learning | Web development,API Design, Algorithm | [개인 리포로 이동](https://github.com/yunyun3599)  |
|   이채림 | Front-end, Devops                  | Web development, Docker               | [개인 리포로 이동](https://github.com/leecr1215)   |
|   박신영 | Front-end, Deep learning           | Web development, Algorithm            | [개인 리포로 이동](https://github.com/shxnyoung)   |
|   이하영 | Back-end, Deep learning            | API Design, Algorithm                 | [개인 리포로 이동](https://github.com/hayoung1214) |
| Ryan Lee | Deep learning                      | Algorithm                             | [개인 리포로 이동](https://github.com/printSANO)   |
|   박근우 | Devops                             | Cloud, Docker, Data Monitoring        | [개인 리포로 이동](https://github.com/Gnu-Kenny)   |
