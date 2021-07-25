# **QUIZRIX(허락 필요)**

* 학습지 이미지 데이터에서 문항정보를 추출해 데이터베이스에 저장 후 해당 내용을 사용자의 브라우저에서 접속 가능하도록하는 플랫폼 
* Quizrix is a platform with a user-friendly interface designed to upload and view workbook problems via classifying different components of the question from a problem image and saving them to a database. 
1. 학습 문제의 이미지를 업로드 방식으로 등록한다. The user uploads the image of the problem.
  <p>
   <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126748956-5bf7503e-575a-4008-83e1-9632de129c2c.png">
	 </p> 
2. 학습지 이미지 데이터에서 딥러닝을 이용하여 문항정보를 추출한다.  The components of the problem are classified through a deep-learning model. (모델 완성 후 수정)
  <p>
   <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126749134-2e804fb4-e62b-4e68-a1aa-4cdc033409c3.png">
	</p> 
	 
<br>

	 최종본 gif 추가


> 본 프로젝트는 코드넛 'QUIZRIX' 사업의 일부 프로토타입 제작을 위해 진행되었습니다. This project was carried out for building a prototype for "Quizrix" of Codnut.
  
  
## **System Architecture ->검사 받고 최종 올려둘게요**

<p align="center">  
  <img src="https://user-images.githubusercontent.com/52441923/126756283-16c5dd0b-8f84-4aab-81f1-b7e4ea4cc171.jpg">
</p>

## **Description**

웹페이지에 문제 이미지를 첨부하면 문항 / 보기 / 선지로 세분화하여 데이터베이스에 저장합니다.
When the problem is uploaded, the problem is classified and separated into three components; question, content, and answer, then is saved into the database.

> 현재 개발 중에 있습니다.

<br>

## **Tech Stack** 

<br>

| 분류          | 기술                                   |  
| :------       | :------------------------------------- |  
| 개발환경      | ![NHN](https://img.shields.io/badge/NHN_Cloud_Ubuntu-20.04-blue?logo=ubuntu) ![S3](https://img.shields.io/badge/S3-green?logo=AmazonS3) ![Docker](https://img.shields.io/badge/docker-blue?logo=docker)  |  
| Front-end     | ![react](https://img.shields.io/badge/react-9cf?logo=react) ![Javascript](https://img.shields.io/badge/javascript-ES6+-yellow?logo=javascript) ![Bootstrap](https://img.shields.io/badge/bootstrap-9cf?logo=bootstrap) ![axios](https://img.shields.io/badge/axios-9cf?color=purple) ![Styled-components](https://img.shields.io/badge/styled_components-DB7093?logo=styled-components)                                  |  
| Back-end      | ![Flask](https://img.shields.io/badge/flask-1.1.2-green?logo=flask) ![Python](https://img.shields.io/badge/python-3.7.6-skyblue?logo=python) ![Gunicorn](https://img.shields.io/badge/gunicorn-darkgreen?logo=gunicorn) ![Postman](https://img.shields.io/badge/postman-pink?logo=postman) ![Swagger](https://img.shields.io/badge/swagger-darkgreen?logo=swagger)              |  
| DB            | ![MongoDB](https://img.shields.io/badge/mongodb-blue?logo=mongodb)                               |
| Deep learning | ![Pytorch](https://img.shields.io/badge/pytorch-blue?logo=pytorch) ![Colab](https://img.shields.io/badge/colab-darkgreen?logo=GoogleColab)                             |
| Etc |  ![Nginx](https://img.shields.io/badge/Nginx-brightgreen?logo=nginx)  ![github](https://img.shields.io/badge/github-gray?logo=github) ![VScode](https://img.shields.io/badge/VScode-blue?logo=visual-studio-code) ![Google Cloud Platform](https://img.shields.io/badge/Google_Cloud_Platform-VM_instance-red?logo=gcp) ![AWS](https://img.shields.io/badge/AWS-EC2_instance-orange?logo=aws)  ![Prometheus](https://img.shields.io/badge/Prometheus-green?logo=Prometheus)    ![Grafana](https://img.shields.io/badge/Grafana-green?logo=Grafana)   ![Redis](https://img.shields.io/badge/Redis-green?logo=redis)            |

## **AI**

### flow
<img width="476" alt="AI Flow" src="https://user-images.githubusercontent.com/80239146/126749561-c724903b-9bf2-4975-968b-6a6f1fe41a71.png">  

<br>

### 결과 Results

- Model 1
  <img width="532" alt="model1" src="https://user-images.githubusercontent.com/80239146/126751834-81adeca3-36f7-48c4-9ea4-e360042f7551.PNG">

- Model 2  
  <img width="571" alt="model2" src="https://user-images.githubusercontent.com/80239146/126751880-3cc7c43f-ee20-4f38-a72e-87b80769dfa7.PNG">
 
  
## **Frontend: React**
#### file tree  install

<br>

## **Backend: Flask**
#### file tree  install


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

###  Docker 

### 배포  

## API  
## gif 이미지 넣는거/ 수정하는거

## 멤버 소개  



<br>

## **Members**

|  이름  | 개발분야              |               담당                |
| :----: | :------------------ | :-------------------------------: |
| 최윤재 | Front-end, Back-end | Web development,API Design, Cloud |
| 이채림 | Front-end           |          Web development          |
| 박신영 | Front-end           |          Web development          |
| 이하영 | Back-end            |            API Design             |
| Ryan Lee | Deep learning            |            Algorithm             |
| 박근우 | Devops              |           Cloud, Docker           |

