한국어 | [English](README_en.md)

<br>

# **✍ QUIZMAKER**

> 본 프로젝트는 'Handshaker' 사업의 일부 프로토타입 제작을 위해 진행되었습니다.

- 학습지 이미지 데이터에서 문항정보를 추출해 데이터베이스에 저장 후 해당 내용을 사용자의 브라우저에서 접속 가능하도록하는 플랫폼

1️⃣ 학습 문제의 이미지를 업로드 방식으로 등록한다.

<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126748956-5bf7503e-575a-4008-83e1-9632de129c2c.png">
 </p>

2️⃣ 학습지 이미지 데이터에서 딥러닝을 이용하여 문항정보를 추출한다.

<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126749134-2e804fb4-e62b-4e68-a1aa-4cdc033409c3.png">
</p>

<br>

     최종본 gif 추가

## **📌System Architecture**

<p align="center">  
  <img src="https://user-images.githubusercontent.com/52441923/126756283-16c5dd0b-8f84-4aab-81f1-b7e4ea4cc171.jpg">
</p>

<br>

## **🛠 Tech Stack**

<br>

| 분류          | 기술                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 개발환경      | ![NHN](https://img.shields.io/badge/NHN_Cloud_Ubuntu-20.04-blue?logo=ubuntu) ![S3](https://img.shields.io/badge/S3-gray?logo=AmazonS3) ![Docker](https://img.shields.io/badge/docker-gray?logo=docker)                                                                                                                                                                                                                                                                                     |
| Front-end     | ![react](https://img.shields.io/badge/react-gray?logo=react) ![Javascript](https://img.shields.io/badge/javascript-ES6+-yellow?logo=javascript) ![Bootstrap](https://img.shields.io/badge/bootstrap-gray?logo=bootstrap) ![axios](https://img.shields.io/badge/axios-gray?logo=axios) ![Styled-components](https://img.shields.io/badge/styled_components-gray?logo=styled-components)                                                                                                     |
| Back-end      | ![Flask](https://img.shields.io/badge/flask-1.1.2-green?logo=flask) ![Python](https://img.shields.io/badge/python-3.7.6-skyblue?logo=python) ![Gunicorn](https://img.shields.io/badge/gunicorn-gray?logo=gunicorn) ![Postman](https://img.shields.io/badge/postman-gray?logo=postman) ![Swagger](https://img.shields.io/badge/swagger-gray?logo=swagger)                                                                                                                                   |
| DB            | ![MongoDB](https://img.shields.io/badge/mongodb-gray?logo=mongodb)                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Deep learning | ![Pytorch](https://img.shields.io/badge/pytorch-gray?logo=pytorch) ![Colab](https://img.shields.io/badge/colab-gray?logo=GoogleColab) ![Yolov5](https://img.shields.io/badge/yolov5-gray?logo=yolov5)                                                                                                                                                                                                                                                                                      |
| Etc           | ![Nginx](https://img.shields.io/badge/Nginx-gray?logo=nginx) ![github](https://img.shields.io/badge/github-gray?logo=github) ![VScode](https://img.shields.io/badge/VScode-gray?logo=visual-studio-code) ![AWS](https://img.shields.io/badge/AWS-EC2_instance-orange?logo=aws) ![Prometheus](https://img.shields.io/badge/Prometheus-gray?logo=Prometheus) ![Grafana](https://img.shields.io/badge/Grafana-gray?logo=Grafana) ![Redis](https://img.shields.io/badge/Redis-gray?logo=redis) |

<br>

## **🧿 PORTS**

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

## **🦾 AI**

### ✔flow

<p align="center">
<img alt="flow" src="https://user-images.githubusercontent.com/80239146/126985473-cae4a4f7-6e58-4a26-b7d5-538a32a361d1.PNG">
</p>

<br>
<br>

### ✔결과

- Model 1

  <img width="532" alt="model1" src="https://user-images.githubusercontent.com/80239146/126751834-81adeca3-36f7-48c4-9ea4-e360042f7551.PNG">

- Model 2

  <img width="571" alt="model2" src="https://user-images.githubusercontent.com/80239146/126751880-3cc7c43f-ee20-4f38-a72e-87b80769dfa7.PNG">

<br>

## **📋 File Tree**

```
📦Mandoo
┣ 📂alertmanager
┃ ┗ 📜config.yml
┣ 📂backend
┃ ┣ 📂models
┃ ┃ ┣ 📂hub
┃ ┣ 📂utils
┃ ┃ ┣ 📂aws
┃ ┃ ┣ 📂flask_rest_api
┃ ┃ ┣ 📂google_app_engine
┃ ┃ ┣ 📂wandb_logging
┃ ┣ 📜Dockerfile
┃ ┣ 📜README.md
┃ ┣ 📜app.py
┃ ┣ 📜choice5_bestweight.pt
┃ ┣ 📜detection.py
┃ ┣ 📜development.py
┃ ┣ 📜kakaoOcr.py
┃ ┣ 📜modelv2.0.pt
┃ ┗ 📜requirements.txt
┣ 📂frontend
┃ ┣ 📂node_modules
┃ ┣ 📂public
┃ ┣ 📂src
┃ ┃ ┣ 📂components
┃ ┃ ┃ ┣ 📂Modals
┃ ┃ ┃ ┃ ┣ 📜Modal.css
┃ ┃ ┃ ┃ ┗ 📜Modal.js
┃ ┃ ┃ ┣ 📜BlankTop.js
┃ ┃ ┃ ┣ 📜Button.js
┃ ┃ ┃ ┣ 📜Header.css
┃ ┃ ┃ ┣ 📜Header.js
┃ ┃ ┃ ┣ 📜logo.PNG
┃ ┃ ┃ ┣ 📜Search.js
┃ ┃ ┃ ┗ 📜Table.js
┃ ┃ ┣ 📂pages
┃ ┃ ┃ ┣ 📜imgIcon.png
┃ ┃ ┃ ┣ 📜Loader.js
┃ ┃ ┃ ┣ 📜Login.js
┃ ┃ ┃ ┣ 📜loginLogo.PNG
┃ ┃ ┃ ┣ 📜MainPage.js
┃ ┃ ┃ ┣ 📜noLogin.PNG
┃ ┃ ┃ ┗ 📜Signup.js
┃ ┃ ┃ ┣ 📜App.js
┃ ┃ ┃ ┣ 📜config.js
┃ ┃ ┣ 📜index.css
┃ ┃ ┗ 📜index.js
┃ ┣ 📜Dockerfile
┃ ┗ 📜README.md
┣ 📂grafana
┃ ┣ 📂provisioning
┃ ┃ ┣ 📂dashboards
┃ ┃ ┃ ┣ 📜dashboard.yml
┃ ┃ ┃ ┣ 📜Docker Prometheus Monitoring.json
┃ ┃ ┃ ┗ 📜FlaskApp_Monitoring.json
┃ ┃ ┗ 📂datasources
┃ ┃ ┃ ┗ 📜datasource.yml
┃ ┗ 📜config.monitoring
┣ 📂nginx
┃ ┗ 📜nginx.conf
┣ 📂prometheus
┃ ┣ 📜alert.rules
┃ ┗ 📜prometheus.yml
┣ 📜.gitignore
┣ 📜docker-compose.yml
┣ 📜LICENSE
┣ 📜README.md
┗ 📜README_en.md
```

<br>

## **🔑 Installation**

> ### Deploy

### **🎡 Github**

- Clone Repository

  ```bash
  git clone https://github.com/2021-Team-E/Mandoo.git
  ```

<br>

### **❄ Front-end** setting

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

### **🌶 Back-end** Setting

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
  APPKEY = <Kakao API>
  ```

### **🐳 Docker**

```bash
docker-compose up —-build
```

<br>

## **📑 Swagger**
[QUIZRIX Swagger Hub link](https://app.swaggerhub.com/apis/mandoo/QUIZRIX/1.0.0)
<p align="center">
<img alt="swagger" src="https://user-images.githubusercontent.com/55429156/127174047-172723ce-e143-4494-bdbb-c94732ef473d.PNG">
</p>
<br>

## **🎡 Git Convention**

### Git-Flow

- master : 제품으로 출시될 수 있는 브랜치
- develop : 다음 출시 버전을 개발하는 브랜치
- feature : 기능을 개발하는 브랜치
- release : 이번 출시 버전을 준비하는 브랜치
- hotfix : 출시 버전에서 발생한 버그를 수정 하는 브랜치

### Process

- 새로운 기능 개발을 위한 `feature` 브랜치를 생성할 때 브랜치 이름은 다음과 같은 규칙으로 생성합니다.
- `feature` 브랜치는 마지막 `develop` 브랜치로부터 생성합니다.
- 꼭 브랜치를 생성하기 전에 `develop` 브랜치를 `pull` 받습니다.

### Branches 명 example

- feature-user (사용자 관련 기능을 구현하는 feature branch)  
  <br>

### **✔Commit message**

커밋 메세지를 작성할 때는 다음과 같은 규칙으로 일관성 있게 작성합니다.

### 1. Commit Message Structure

기본적으로 커밋 메세지는 아래와 같이 제목 / 본문 / 꼬리말로 구성합니다.

```xml
type : subject

body

```

### 2. Commit Type

- feat : 새로운 기능 추가
- fix : 버그 수정, 기능 수정
- docs : 문서 수정
- refactor : 코드 리팩토링 (변수명 수정 등)
- test : 테스트 코드, 리팩토링 테스트 코드 추가
- style : 코드 스타일 변경, 코드 자체 변경이 없는 경우, 주석 추가
- remove : 파일 또는 코드, 리소스 제거
- resource : 이미지 리소스, prefab 등의 코드와 상관없는 리소스 추가

### 3. Subject

- 제목은 50자를 넘기지 않고, 대문자로 작성하고 마침표를 붙이지 않습니다.
- 과거시제를 사용하지 않고 명령어로 작성합니다.

예시

```xml
feat : Add translation to missing strings
feat : Disable publishing
feat : Sort list context menu
feat : Resize minimize/delete handle icons so they take up the entire topbar
fix : Fix typo in cleanup.sh file
```

### 4. Body

- 선택사항이기 때문에 모든 커밋에 본문내용을 작성할 필요는 없습니다.
- 부연설명이 필요하거나 커밋의 이유를 설명할 경우 작성합니다.
- 제목과 구분되기 위해 한칸을 띄워 작성합니다.
- 각 줄은 72자를 넘기지 않습니다.
- **본문은 꼭 영어로 작성할 필요는 없습니다.**

### **✔git rebase**

원격 저장소에 Pull Request하기 전 프로젝트의 히스토리를 다듬습니다.  
`rebase` 를 시행하기 전 원격저장소에서 `develop` 브랜치를 `pull` 받아 원격 저장소에 그동안 반영된 커밋을 가져옵니다.

```bash
git checkout develop
git pull
```

### 현재 작업중인 feature 브랜치의 커밋을 develop 에 rebase 하기

```bash
git rebase develop feature/feature1
```

💡 **주의**

이미 원격 저장소에 push한 커밋은 절대 rebase하면 안됩니다.

Rebase는 기존의 커밋을 그대로 사용하는 것이 아니라 내용은 같지만 다른 커밋을 새로 만듭니다.  
<br>

## **👪 Members**

| 이름       | 개발분야                           | 담당                                         | 소개페이지                                         |
| ---------- | ---------------------------------- | -------------------------------------------- | -------------------------------------------------- |
| 🦦최윤재   | Front-end, Back-end, Deep learning | Web development,API Design, Data Engineering | [개인 리포로 이동](https://github.com/yunyun3599)  |
| 🐥이채림   | Front-end, Devops                  | Web development, Docker                      | [개인 리포로 이동](https://github.com/leecr1215)   |
| 🦩박신영   | Front-end, Deep learning           | Web development, Algorithm                   | [개인 리포로 이동](https://github.com/shxnyoung)   |
| 🐹이하영   | Back-end, Deep learning            | API Design, Data Engineering                 | [개인 리포로 이동](https://github.com/hayoung1214) |
| 🦉Ryan Lee | Deep learning                      | Algorithm                                    | [개인 리포로 이동](https://github.com/printSANO)   |
| 🐢박근우   | Devops                             | Cloud, Docker, Data Monitoring               | [개인 리포로 이동](https://github.com/Gnu-Kenny)   |
