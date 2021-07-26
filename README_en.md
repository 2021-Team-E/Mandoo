[한국어](README.md) | English

------------------------------------------------------------------------------------------

# **QUIZRIX(허락 필요)**

- Quizrix is a platform with a user-friendly interface designed to upload and view workbook problems via classifying different components of the question from a problem image and saving them to a database.

1. The user uploads the image of the problem.
<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126748956-5bf7503e-575a-4008-83e1-9632de129c2c.png">
 </p>
2. The components of the problem are classified through a deep-learning model. (모델 완성 후 수정)
<p>
 <img width="700" alt="quizrix_imageupload" src="https://user-images.githubusercontent.com/52441923/126749134-2e804fb4-e62b-4e68-a1aa-4cdc033409c3.png">
</p>

<br>

     최종본 gif 추가

> This project was carried out for building a prototype for "Quizrix" of Codnut.

## **System Architecture ->검사 받고 최종 올려둘게요**

<p align="center">  
  <img src="https://user-images.githubusercontent.com/52441923/126756283-16c5dd0b-8f84-4aab-81f1-b7e4ea4cc171.jpg">
</p>

## **Description**

The problem is classified and separated into three components; question, content, and answer, and then they save into the database.

> 현재 개발 중에 있습니다.

<br>

## **Tech Stack**

<br>

| Category          | Tools                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dev. Environment| ![NHN](https://img.shields.io/badge/NHN_Cloud_Ubuntu-20.04-blue?logo=ubuntu) ![S3](https://img.shields.io/badge/S3-green?logo=AmazonS3) ![Docker](https://img.shields.io/badge/docker-blue?logo=docker)                                                                                                                                                                                                                                                                                                                                                                                                    |
| Front-end     | ![react](https://img.shields.io/badge/react-9cf?logo=react) ![Javascript](https://img.shields.io/badge/javascript-ES6+-yellow?logo=javascript) ![Bootstrap](https://img.shields.io/badge/bootstrap-9cf?logo=bootstrap) ![axios](https://img.shields.io/badge/axios-9cf?color=purple) ![Styled-components](https://img.shields.io/badge/styled_components-DB7093?logo=styled-components)                                                                                                                                                                                                                    |
| Back-end      | ![Flask](https://img.shields.io/badge/flask-1.1.2-green?logo=flask) ![Python](https://img.shields.io/badge/python-3.7.6-skyblue?logo=python) ![Gunicorn](https://img.shields.io/badge/gunicorn-darkgreen?logo=gunicorn) ![Postman](https://img.shields.io/badge/postman-pink?logo=postman) ![Swagger](https://img.shields.io/badge/swagger-darkgreen?logo=swagger)                                                                                                                                                                                                                                         |
| DB            | ![MongoDB](https://img.shields.io/badge/mongodb-blue?logo=mongodb)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Deep learning | ![Pytorch](https://img.shields.io/badge/pytorch-blue?logo=pytorch) ![Colab](https://img.shields.io/badge/colab-darkgreen?logo=GoogleColab)                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Etc           | ![Nginx](https://img.shields.io/badge/Nginx-brightgreen?logo=nginx) ![github](https://img.shields.io/badge/github-gray?logo=github) ![VScode](https://img.shields.io/badge/VScode-blue?logo=visual-studio-code) ![Google Cloud Platform](https://img.shields.io/badge/Google_Cloud_Platform-VM_instance-red?logo=gcp) ![AWS](https://img.shields.io/badge/AWS-EC2_instance-orange?logo=aws) ![Prometheus](https://img.shields.io/badge/Prometheus-green?logo=Prometheus) ![Grafana](https://img.shields.io/badge/Grafana-green?logo=Grafana) ![Redis](https://img.shields.io/badge/Redis-green?logo=redis) |

## **PORTS**

| Name             | Port       | Description                                                                                                                                   |
| ---------------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Nginx            | 80         | HTTP Server and porxy that is simple but produces high performance.             |
| React(on Nginx)  | 80, 3000   | Provides a UI for uploading, viewing, and saving data provided by the classification model.|
| Flask + Gunicorn | 8000, 5000 | It is the main server for QUIZRIX and it connects web, Cloud Storage, and database in the center.                                                 |
| Mongo DB         | 27017      | Database                                                                                                                                      |
| Grafana          | 3001       | Provides a visual dashboard from the metrics data provided by cAdvisorm Prometheus, and NodeExporter. |
| cAdvisor         | 8080       | Measures resource usage by the docker containers and returns it as a time series data.         |
| Prometheus       | 9090       | Monitors and alerts based on the time series data collected from cAdvisor and NodeExporter  |
| Node Exporter    | 9100       | Collects host-related data such as, CPU, memory, disk, and network, and reveals it to the API.          |

<br>

## **AI**

### flow

<img width="476" alt="AI Flow" src="https://user-images.githubusercontent.com/80239146/126749561-c724903b-9bf2-4975-968b-6a6f1fe41a71.png">

<br>

### Results

- Model 1 <br>
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
  #Create directory for tesseract.exe in server env.
  pytesseract.pytesseract.tesseract_cmd="/usr/bin/tesseract"
  ```

- requirements.txt  
  Libraries installed separately by Dockerfile is commented

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

## Team Members

<br>

## **Members**

|  Name     | Developement Field          | Skills in Charge                | Personal Bio                  |
| ------- | ------------------------------- | --------------------------------- | --------------------------------------- |
| Laura Y. Choi | Front-end, Back-end, Deep learning | Web development,API Design, Data Engineering | [Move to Personal Bio](https://github.com/yunyun3599)  |
| Julia C. Lee | Front-end, Devops                  | Web development, Docker               | [Move to Personal Bio](https://github.com/leecr1215)   |
| Claire S. Park | Front-end, Deep learning           | Web development, Algorithm            | [Move to Personal Bio](https://github.com/shxnyoung)   |
|Julie H. Lee | Back-end, Deep learning            | API Design, Data Engineering                | [Move to Personal Bio](https://github.com/hayoung1214) |
| Ryan H. Lee | Deep learning                      | Algorithm                             | [Move to Personal Bio](https://github.com/printSANO)   |
| Kenny G. Park | Devops                             | Cloud, Docker, Data Monitoring        | [Move to Personal Bio](https://github.com/Gnu-Kenny)   |
